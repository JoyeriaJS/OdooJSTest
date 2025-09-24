# -*- coding: utf-8 -*-
import base64, xlrd, requests
from io import BytesIO
from PIL import Image

from odoo import api, models, fields, _
from odoo.exceptions import UserError, AccessError

class ImportarProductosWizard(models.TransientModel):
    _name = 'importar.productos.wizard'
    _description = 'Importar productos desde Excel'

    archivo  = fields.Binary(string='Archivo Excel', required=True)
    filename = fields.Char(string='Nombre del archivo')

    # -----------------------
    # Helpers
    # -----------------------
    def safe_float(self, val):
        if not self.env.user.has_group('base.group_system'):
            raise AccessError("Sólo los administradores pueden generar este reporte.")
        try:
            return float(val)
        except Exception:
            return 0.0

    def resize_image_128(self, img_bytes):
        if not self.env.user.has_group('base.group_system'):
            raise AccessError("Sólo los administradores pueden generar este reporte.")
        try:
            img = Image.open(BytesIO(img_bytes)).convert("RGB")
            img = img.resize((128,128), Image.LANCZOS)
            buf = BytesIO()
            img.save(buf, 'JPEG')
            return base64.b64encode(buf.getvalue())
        except Exception:
            return False

    def _normalize_barcode(self, val):
        """Convierte el valor del Excel a un string: quita .0 y espacios; preserva dígitos.
        Si el código es alfanumérico, se conserva tal cual (sin recortar a solo dígitos)."""
        if val is None:
            return ''
        s = str(int(val)).strip() if isinstance(val, float) and float(val).is_integer() else str(val).strip()
        # Quitar sufijo “.0” (ej: '1812001.0' -> '1812001')
        if s.endswith('.0'):
            s = s[:-2]
        # No elimino letras por si usas códigos alfanuméricos (EAN/UPC suelen ser numéricos, pero por si acaso)
        return s

    def _find_col(self, sheet, candidates, default_idx):
        """Intenta encontrar la columna por encabezado (en las primeras 3 filas). 
        candidates: lista de posibles encabezados (case-insensitive).
        default_idx: índice por defecto si no encuentra nada.
        """
        cand_lower = [c.lower() for c in candidates]
        top_rows = min(3, sheet.nrows)
        for r in range(top_rows):
            for c in range(sheet.ncols):
                try:
                    text = str(sheet.cell_value(r, c)).strip().lower()
                except Exception:
                    text = ''
                if text in cand_lower:
                    return c
        return default_idx

    @api.model
    def _get_pricelists(self):
        if not self.env.user.has_group('base.group_system'):
            raise AccessError("Sólo los administradores pueden generar este reporte.")
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

    # -----------------------
    # Acción principal
    # -----------------------
    def importar_productos(self):
        if not self.env.user.has_group('base.group_system'):
            raise AccessError("Sólo los administradores pueden generar este reporte.")
        if not self.archivo:
            raise UserError(_("Adjunta primero un archivo Excel."))

        data = base64.b64decode(self.archivo)
        book = xlrd.open_workbook(file_contents=data)
        sheet = book.sheet_by_name("Productos") if "Productos" in book.sheet_names() else book.sheet_by_index(0)

        # Índices base (los tuyos)
        cols = {
            'code':       9,
            'name':       1,
            'weight':     3,
            'costo':      4,
            'pub':        5,
            'mayorista':  6,
            'preferente': 7,
            'interno':    8,
            'barcode':   15,   # asumido, pero lo recalculamos abajo si está movido
            'image_url': 16,
            'attr_name': 17,
            'attr_vals': 18,
            'pos':       19,
        }

        # >>> Ajuste robusto: si cambiaron las columnas, detectar por encabezado <<<
        cols['barcode'] = self._find_col(
            sheet,
            candidates=['codbar', 'códbar', 'codigo de barras', 'código de barras', 'barcode', 'ean13'],
            default_idx=cols['barcode']
        )

        pricelists = self._get_pricelists()
        Product    = self.env['product.template']
        ProdVar    = self.env['product.product']
        Category   = self.env['product.category']
        PosCateg   = self.env['pos.category']
        Attr       = self.env['product.attribute']
        AttrVal    = self.env['product.attribute.value']
        PrItem     = self.env['product.pricelist.item']

        duplicates_code    = set()
        duplicates_barcode = set()
        imported           = 0

        # Datos desde la fila 3 (0-based = 3) como ya tenías
        for row_idx in range(3, sheet.nrows):
            row = sheet.row(row_idx)
            code = str(row[cols['code']].value).strip().upper()
            if not code or code.lower().startswith('code'):
                continue

            # Saltar códigos duplicados
            if Product.search([('default_code', '=', code)], limit=1):
                duplicates_code.add(code)
                continue

            # Leer y normalizar BARCODE
            raw_barcode = row[cols['barcode']].value if cols['barcode'] < sheet.ncols else ''
            barcode = self._normalize_barcode(raw_barcode)

            # Saltar barcodes duplicados (si existe)
            if barcode and ProdVar.search([('barcode', '=', barcode)], limit=1):
                duplicates_barcode.add(barcode)
                barcode = ''  # evita fallo y sigue creando el producto sin codbar
                # (si prefieres saltar el producto, usa "continue")

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

            categ = Category.search([('name', '=', cat_name)], limit=1) or Category.create({'name': cat_name})
            pos_categ = PosCateg.search([('name', '=', cat_name)], limit=1) or PosCateg.create({'name': cat_name})

            # Procesar imagen
            img_data = False
            if img_url.startswith('http'):
                try:
                    r = requests.get(img_url, timeout=5)
                    if r.ok:
                        img_data = self.resize_image_128(r.content)
                except Exception:
                    pass

            # Procesar atributos (si tu Excel trae muchos valores en una fila, generará varias variantes)
            attr_lines = []
            if attr_name and attr_vals:
                att = Attr.search([('name', '=', attr_name)], limit=1) or Attr.create({'name': attr_name})
                val_ids = []
                for v in (x.strip() for x in attr_vals.split(',') if x.strip()):
                    av = AttrVal.search([('name', '=', v), ('attribute_id', '=', att.id)], limit=1) \
                         or AttrVal.create({'name': v, 'attribute_id': att.id})
                    val_ids.append(av.id)
                if val_ids:
                    attr_lines = [(0, 0, {'attribute_id': att.id, 'value_ids': [(6, 0, val_ids)]})]

            # Crear plantilla
            tmpl_vals = {
                'default_code':       code,
                'name':               name,
                'categ_id':           categ.id,
                'type':               'product',
                'barcode':            barcode,   # lo dejamos también en template (no molesta)
                'list_price':         pub_pr,
                'standard_price':     cost_pr,
                'weight':             weight,
                'available_in_pos':   True,
                'image_1920':         img_data,
                'attribute_line_ids': attr_lines or False,
            }
            tmpl = Product.create(tmpl_vals)

            # POS categoría
            if 'pos_categ_ids' in Product._fields:
                tmpl.write({'pos_categ_ids': [(4, pos_categ.id)]})

            imported += 1
            if imported % 20 == 0:
                self.env.cr.commit()

            # --- PROPAGAR BARCODE A VARIANTES ---
        if barcode:
            if getattr(tmpl, 'product_variant_count', 0) == 1:
                # Caso tradicional: una sola variante
                if not tmpl.product_variant_id.barcode:
                    tmpl.product_variant_id.barcode = barcode
            else:
                # NUEVO: múltiples variantes y el Excel trajo un único barcode.
                # Copiamos el mismo código a todas las variantes sin código
                for var in tmpl.product_variant_ids:
                    if not var.barcode:
                        var.barcode = barcode

            # Reglas de precio
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

        # Notificación
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
