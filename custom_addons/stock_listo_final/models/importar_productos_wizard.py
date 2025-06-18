from odoo import models, fields
import base64
import xlrd
import requests
from PIL import Image
from io import BytesIO

class ImportarProductosWizard(models.TransientModel):
    _name = 'importar.productos.wizard'
    _description = 'Importar productos desde Excel'

    archivo = fields.Binary(string='Archivo Excel')
    filename = fields.Char(string='Nombre del archivo')

    def safe_float(self, val):
        try:
            return float(val)
        except Exception:
            return 0.0

    def resize_image_128(self, img_bytes):
        """Redimensiona imagen a 128x128 px y retorna base64."""
        try:
            image = Image.open(BytesIO(img_bytes)).convert("RGB")
            image = image.resize((128, 128), Image.LANCZOS)
            buf = BytesIO()
            image.save(buf, format='JPEG')
            return base64.b64encode(buf.getvalue())
        except Exception:
            return False

    def importar_productos(self):
        if not self.archivo:
            return
        data = base64.b64decode(self.archivo)
        book = xlrd.open_workbook(file_contents=data)
        sheet = book.sheet_by_name("Productos")

        Product = self.env['product.template']
        Category = self.env['product.category']
        Attr = self.env['product.attribute']
        AttrVal = self.env['product.attribute.value']
        PrList = self.env['product.pricelist']
        PrItem = self.env['product.pricelist.item']

        duplicates = []
        imported = 0

        # Columnas de tarifas por nombre de lista
        price_lists = {
            'Pública': 5,
            'Mayorista': 6,
            'Preferente': 7,
            'Interno': 8,
        }

        # Asegurar listas de precio existentes
        for pl_name in price_lists:
            PrList.search([('name', '=', pl_name)], limit=1) or PrList.create({
                'name': pl_name,
                'currency_id': self.env.user.company_id.currency_id.id,
            })

        for row in range(3, sheet.nrows):
            code = str(sheet.cell(row, 9).value).strip()
            name = str(sheet.cell(row, 1).value).strip()
            weight = self.safe_float(sheet.cell(row, 3).value)
            cost = self.safe_float(sheet.cell(row, 4).value)
            barcode = str(sheet.cell(row, 15).value).strip()
            img_url = str(sheet.cell(row, 16).value).strip()
            attr_name = str(sheet.cell(row, 17).value).strip()
            attr_vals = str(sheet.cell(row, 18).value).strip()

            # Categoría compuesta
            metal = str(sheet.cell(row, 10).value).strip()
            nacimp = str(sheet.cell(row, 11).value).strip()
            externa = str(sheet.cell(row, 12).value).strip()
            tipo = str(sheet.cell(row, 14).value).strip()
            cat_name = f"{metal} / {nacimp} / {externa} / {tipo}"
            categ = Category.search([('name','=',cat_name)], limit=1) or Category.create({'name': cat_name})

            # Imagen
            img_data = False
            if img_url.startswith('http'):
                try:
                    resp = requests.get(img_url, timeout=10)
                    if resp.status_code == 200:
                        img_data = self.resize_image_128(resp.content)
                except:
                    pass

            # Duplicados
            if code and Product.search([('default_code','=',code)], limit=1):
                duplicates.append(code)
                continue
            if name and Product.search([('name','=',name)], limit=1):
                duplicates.append(name)
                continue

            # Atributos
            attr_lines = []
            if attr_name and attr_vals:
                att = Attr.search([('name','=',attr_name)], limit=1) or Attr.create({'name': attr_name})
                val_ids = []
                for v in [v.strip() for v in attr_vals.split(',') if v.strip()]:
                    av = AttrVal.search([
                        ('name','=',v),('attribute_id','=',att.id)
                    ], limit=1) or AttrVal.create({'name': v, 'attribute_id': att.id})
                    val_ids.append(av.id)
                if val_ids:
                    attr_lines = [(0,0,{'attribute_id': att.id,'value_ids': [(6,0,val_ids)]})]

            # Leer tarifas desde Excel
            tarifas = {pl_name: self.safe_float(sheet.cell(row, idx).value)
                       for pl_name, idx in price_lists.items()}

            # Crear plantilla
            tmpl = Product.create({
                'default_code': code or f"CODE%05d" % (Product.search_count([])+1),
                'name': name,
                'categ_id': categ.id,
                'type': 'product',
                'barcode': barcode,
                'list_price': tarifas.get('Pública', 0.0),
                'standard_price': cost,
                'weight': weight,
                'image_1920': img_data,
                'attribute_line_ids': attr_lines or False,
            })
            imported += 1

            # Crear reglas de precio
            for pl_name, price in tarifas.items():
                if price > 0:
                    pl = PrList.search([('name','=',pl_name)], limit=1)
                    PrItem.create({
                        'pricelist_id':     pl.id,
                        'product_tmpl_id':  tmpl.id,
                        'applied_on':       '1_product',
                        'compute_price':    'fixed',
                        'fixed_price':      price,
                    })

        # Notificación al usuario
        msg = f"{imported} productos importados."
        if duplicates:
            uniques = list(dict.fromkeys(duplicates))
            msg += f" Omitidos {len(uniques)} duplicados: {', '.join(uniques)}."

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': "Importación Productos",
                'message': msg,
                'sticky': False,
            }
        }
