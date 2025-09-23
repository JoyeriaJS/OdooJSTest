# -*- coding: utf-8 -*-
import base64, xlrd, requests
from io import BytesIO
from PIL import Image

from odoo import api, models, fields, _
from odoo.exceptions import UserError
from odoo.exceptions import AccessError

class ImportarProductosWizard(models.TransientModel):
    _name = 'importar.productos.wizard'
    _description = 'Importar productos desde Excel'

    archivo  = fields.Binary(string='Archivo Excel', required=True)
    filename = fields.Char(string='Nombre del archivo')

    def safe_float(self, val):
        # Sólo administradores
        if not self.env.user.has_group('base.group_system'):
            raise AccessError("Sólo los administradores pueden generar este reporte.")
        try:
            return float(val)
        except:
            return 0.0

    def resize_image_128(self, img_bytes):
        # Sólo administradores
        if not self.env.user.has_group('base.group_system'):
            raise AccessError("Sólo los administradores pueden generar este reporte.")
        try:
            img = Image.open(BytesIO(img_bytes)).convert("RGB")
            img = img.resize((128,128), Image.LANCZOS)
            buf = BytesIO()
            img.save(buf, 'JPEG')
            return base64.b64encode(buf.getvalue())
        except:
            return False

    # --- NUEVO: normalizador mínimo para CodBar del Excel ---
    def _normalize_barcode(self, val):
        """Convierte el valor de Excel a un string de dígitos (sin .0, sin espacios)."""
        if val is None:
            return ''
        # Si viene como número (float/int), convertir a entero si es xx.0
        if isinstance(val, (int, float)):
            try:
                if float(val).is_integer():
                    val = int(val)
            except Exception:
                pass
            s = str(val).strip()
        else:
            s = str(val).strip()

        # Casos típicos: '1812001.0' -> '1812001'
        if s.endswith('.0'):
            s = s[:-2]

        # Quitar espacios y dejar sólo dígitos
        s = ''.join(ch for ch in s if ch.isdigit())
        return s

    @api.model
    def _get_pricelists(self):
        # Sólo administradores
        if not self.env.user.has_group('base.group_system'):
            raise AccessError("Sólo los administradores pueden generar este reporte.")
        """Garantiza existencia de cada pricelist y las devuelve."""
        names = ['Pública','Punto de venta','Mayorista','Preferente','Interno (CLP)']
        PrList = self.env['product.pricelist']
        res = {}
        for name in names:
            pl = PrList.search([('name','=', name)], limit=1)
            if not pl:
                pl = PrList.create({
                    'name':        name,
                    'currency_id': self.env.company.currency_id.id,
                })
            res[name] = pl
        return res

    def importar_productos(self):
        # Sólo administradores
        if not self.env.user.has_group('base.group_system'):
            raise AccessError("Sólo los administradores pueden generar este reporte.")
        if not self.archivo:
            raise UserError(_("Adjunta primero un archivo Excel."))
        data = base64.b64decode(self.archivo)
        book = xlrd.open_workbook(file_contents=data)
        sheet = book.sheet_by_name("Productos") if "Productos" in book.sheet_names() else book.sheet_by_index(0)

        # Columnas de tu hoja (ajusta índices si cambien)
        cols = {
            'code':       9,
            'name':       1,
            'weight':     3,
            'costo':      4,
            'pub':        5,
            'mayorista':  6,
            'preferente': 7,
            'interno':    8,
            'barcode':   15,
            'image_url': 16,
            'attr_name': 17,
            'attr_vals': 18,
            'pos':       19,
        }

        pricelists    = self._get_pricelists()
        Product       = self.env['product.template']
        ProdVar       = self.env['product.product']
        Category      = self.env['product.category']
        PosCateg      = self.env['pos.category']
        Attr          = self.env['product.attribute']
        AttrVal       = self.env['product.attribute.value']
        PrItem        = self.env['product.pricelist.item']

        duplicates_code    = set()
        duplicates_barcode = set()
        imported           = 0

        for row_idx in range(3, sheet.nrows):
            row = sheet.row(row_idx)
            code = str(row[cols['code']].value).strip().upper()
            if not code or code.lower().startswith('code'):
                continue

            # Saltar códigos duplicados
            if Product.search([('default_code','=', code)], limit=1):
                duplicates_code.add(code)
                continue

            # --- CAMBIO: normalizar el barcode leído del Excel ---
            raw_barcode = row[cols['barcode']].value
            barcode = self._normalize_barcode(raw_barcode)

            # Saltar barcodes duplicados (si existe y está normalizado)
            if barcode and ProdVar.search([('barcode','=', barcode)], limit=1):
                duplicates_barcode.add(barcode)
                continue

            name       = str(row[cols['name']].value).strip()
            weight     = self.safe_float(row[cols['weight']].value)
            cost_pr    = self.safe_float(row[cols['costo']].value)
            interno_pr = self.safe_float(row[cols['interno']].value)
            pub_pr     = self.safe_float(row[cols['pub']].value)
            pos_pr     = self.safe_float(row[cols['pos']].value)
            may_pr     = self.safe_float(row[cols['mayorista']].value)
            pref_pr    = self.safe_float(row[cols['preferente']].value)
            img_url    = str(row[cols['image_url']].value).strip()
            attr_name  = str(row[cols['attr_name']].value).strip()
            attr_vals  = str(row[cols['attr_vals']].value).strip()

            # Categoría compuesta
            metal   = str(row[10].value).strip()
            nacimp  = str(row[11].value).strip()
            externa = str(row[12].value).strip()
            tipo    = str(row[14].value).strip()
            cat_name = f"{metal} / {nacimp} / {externa} / {tipo}"

            categ = Category.search([('name','=', cat_name)], limit=1) or Category.create({'name': cat_name})
            pos_categ = PosCateg.search([('name','=', cat_name)], limit=1) or PosCateg.create({'name': cat_name})

            # Procesar imagen
            img_data = False
            if img_url.startswith('http'):
                try:
                    r = requests.get(img_url, timeout=5)
                    if r.ok:
                        img_data = self.resize_image_128(r.content)
                except:
                    pass

            # Procesar atributos
            attr_lines = []
            if attr_name and attr_vals:
                att = Attr.search([('name','=', attr_name)], limit=1) or Attr.create({'name': attr_name})
                val_ids = []
                for v in (x.strip() for x in attr_vals.split(',') if x.strip()):
                    av = AttrVal.search([('name','=', v), ('attribute_id','=', att.id)], limit=1) \
                         or AttrVal.create({'name': v, 'attribute_id': att.id})
                    val_ids.append(av.id)
                if val_ids:
                    attr_lines = [(0, 0, {'attribute_id': att.id, 'value_ids': [(6, 0, val_ids)]})]

            # Construir valores para la plantilla
            tmpl_vals = {
                'default_code':       code,
                'name':               name,
                'categ_id':           categ.id,
                'type':               'product',
                'barcode':            barcode,     # <- ya normalizado
                'list_price':         pub_pr,
                'standard_price':     cost_pr,
                'weight':             weight,
                'available_in_pos':   True,
                'image_1920':         img_data,
                'attribute_line_ids': attr_lines or False,
            }
            # Crear la plantilla
            tmpl = Product.create(tmpl_vals)
            # Asignar categoría POS al template a través de pos_categ_ids
            if 'pos_categ_ids' in Product._fields:
                tmpl.write({'pos_categ_ids': [(4, pos_categ.id)]})
            imported += 1
            if imported % 20 == 0:
                self.env.cr.commit()

            # --- NUEVO: Propagar barcode a la variante única (para etiquetas) ---
            if barcode and getattr(tmpl, 'product_variant_count', 0) == 1:
                if not tmpl.product_variant_id.barcode:
                    tmpl.product_variant_id.barcode = barcode

            # Crear reglas de precio
            rules = {
                'Pública':        pub_pr,
                'Punto de venta': pos_pr,
                'Mayorista':      may_pr,
                'Preferente':     pref_pr,
                'Interno (CLP)':  interno_pr,
            }
            for name_list, price in rules.items():
                if price > 0.0:
                    PrItem.create({
                        'pricelist_id':    pricelists[name_list].id,
                        'product_tmpl_id': tmpl.id,
                        'applied_on':      '1_product',
                        'compute_price':   'fixed',
                        'fixed_price':     price,
                    })

        # Notificación final
        msg = _("%d productos importados.") % imported
        if duplicates_code:
            msg += _(" Se omitieron códigos duplicados: %s") % ', '.join(sorted(duplicates_code))
        if duplicates_barcode:
            msg += _(" Se omitieron barcodes duplicados: %s") % ', '.join(sorted(duplicates_barcode))
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title':   _("Importación finalizada"),
                'message': msg,
                'sticky':  False,
            }
        }
