# -*- coding: utf-8 -*-
import base64
import xlrd
import requests
from io import BytesIO
from PIL import Image

from odoo import api, models, fields
from odoo.exceptions import UserError

class ImportarProductosWizard(models.TransientModel):
    _name = 'importar.productos.wizard'
    _description = 'Importar productos desde Excel'

    archivo   = fields.Binary(string='Archivo Excel', required=True)
    filename  = fields.Char(string='Nombre del archivo')

    def safe_float(self, val):
        try:
            return float(val)
        except Exception:
            return 0.0

    def resize_image_128(self, img_bytes):
        try:
            image = Image.open(BytesIO(img_bytes)).convert("RGB")
            image = image.resize((128, 128), Image.LANCZOS)
            buf = BytesIO()
            image.save(buf, format='JPEG')
            return base64.b64encode(buf.getvalue())
        except Exception:
            return False

    @api.model
    def _get_pricelists(self):
        """Busca o crea las pricelists y devuelve un dict { nombre: record }."""
        names = {
            'Pública':    None,
            'Mayorista':  None,
            'Preferente': None,
            'Interno (CLP)': None,
        }
        PrList = self.env['product.pricelist']
        for name in list(names):
            pl = PrList.search([('name', '=', name)], limit=1)
            if not pl:
                pl = PrList.create({
                    'name':        name,
                    'currency_id': self.env.user.company_id.currency_id.id,
                })
            names[name] = pl
        return names

    def importar_productos(self):
        if not self.archivo:
            raise UserError("Adjunta primero un archivo Excel.")
        data = base64.b64decode(self.archivo)
        book = xlrd.open_workbook(file_contents=data)
        try:
            sheet = book.sheet_by_name("Productos")
        except:
            sheet = book.sheet_by_index(0)

        # Prepárate para crear
        Product  = self.env['product.template']
        Category = self.env['product.category']
        Attr     = self.env['product.attribute']
        AttrVal  = self.env['product.attribute.value']
        pricelists = self._get_pricelists()

        # Mapea nombre de columna → índice en tu hoja
        # Ajusta estos índices a la estructura real de tu Excel
        cols = {
            'default_code':       9,
            'name':               1,
            'weight':             3,
            'interno_price':      8,
            'barcode':           15,
            'image_url':         16,
            'attr_name':         17,
            'attr_vals':         18,
            # tarifas:
            'Pública':           5,
            'Mayorista':         6,
            'Preferente':        7,
            'Interno (CLP)':     8,
        }

        duplicates = set()
        imported   = 0

        # Filas de datos (suponemos encabezado en fila 2→index 2; datos a partir de index 3)
        for row_idx in range(3, sheet.nrows):
            row = sheet.row(row_idx)
            code = str(row[cols['default_code']].value).strip().upper()
            name = str(row[cols['name']].value).strip()
            if not code or code.lower().startswith('code'): 
                continue  # salta filas vacías o de ejemplo

            # Control de duplicados
            if Product.search([('default_code','=',code)], limit=1):
                duplicates.add(code)
                continue

            # Datos base
            weight       = self.safe_float(row[cols['weight']].value)
            interno_cost = self.safe_float(row[cols['interno_price']].value)
            barcode      = str(row[cols['barcode']].value).strip()
            img_url      = str(row[cols['image_url']].value).strip()
            attr_name    = str(row[cols['attr_name']].value).strip()
            attr_vals    = str(row[cols['attr_vals']].value).strip()

            # Categoría combinada (ajusta si tu lógica varía)
            metal   = str(row[10].value).strip()
            nacimp  = str(row[11].value).strip()
            externa = str(row[12].value).strip()
            tipo    = str(row[14].value).strip()
            cat_name = f"{metal} / {nacimp} / {externa} / {tipo}"
            categ = Category.search([('name','=',cat_name)], limit=1) or Category.create({'name': cat_name})

            # Imagen
            img_data = False
            if img_url.startswith('http'):
                try:
                    resp = requests.get(img_url, timeout=5)
                    if resp.ok:
                        img_data = self.resize_image_128(resp.content)
                except:
                    pass

            # Atributos
            attr_lines = []
            if attr_name and attr_vals:
                att = Attr.search([('name','=',attr_name)], limit=1) \
                      or Attr.create({'name':attr_name})
                val_ids = []
                for v in [x.strip() for x in attr_vals.split(',') if x.strip()]:
                    av = AttrVal.search([('name','=',v),('attribute_id','=',att.id)], limit=1) \
                         or AttrVal.create({'name':v,'attribute_id':att.id})
                    val_ids.append(av.id)
                if val_ids:
                    attr_lines = [(0,0,{'attribute_id':att.id,'value_ids':[(6,0,val_ids)]})]

            # Tarifas del Excel
            tarifas = {
                name: self.safe_float(row[idx].value)
                for name, idx in cols.items()
                if name in pricelists and idx < len(row)
            }

            # Crea la plantilla de producto
            tmpl = Product.create({
                'default_code':     code,
                'name':             name,
                'categ_id':         categ.id,
                'type':             'product',
                'barcode':          barcode,
                'list_price':       tarifas.get('Pública', 0.0),
                'standard_price':   interno_cost,
                'weight':           weight,
                'image_1920':       img_data,
                'attribute_line_ids': attr_lines or False,
            })
            imported += 1

            # Crea cada regla de precio sólo si price > 0
            for pl_name, price in tarifas.items():
                if pl_name not in pricelists or price <= 0.0:
                    continue
                PrItem = self.env['product.pricelist.item']
                PrItem.create({
                    'pricelist_id':    pricelists[pl_name].id,
                    'product_tmpl_id': tmpl.id,
                    'applied_on':      '1_product',
                    'compute_price':   'fixed',
                    'fixed_price':     price,
                })

        # Feedback al usuario
        msg = _(f"{imported} productos importados.")
        if duplicates:
            msg += _(" Omitidos duplicados: %s") % ', '.join(sorted(duplicates))
        return {
            'type': 'ir.actions.client',
            'tag':  'display_notification',
            'params': {
                'title':   _("Importación finalizada"),
                'message': msg,
                'sticky':  False,
            }
        }
