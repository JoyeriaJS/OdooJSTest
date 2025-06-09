from odoo import models, fields
import base64
import xlrd
import requests
from PIL import Image
from io import BytesIO

class ImportarProductosWizard(models.TransientModel):
    _name = 'importar.productos.wizard'
    _description = 'Importar productos desde Excel'

    archivo = fields.Binary(string='Archivo Excel', required=False)
    filename = fields.Char(string='Nombre del archivo')

    def safe_float(self, val):
        try:
            return float(val)
        except Exception:
            return 0.0

    def resize_image_128(self, img_bytes):
        """Redimensiona imagen a 128x128 px y retorna base64."""
        try:
            image = Image.open(BytesIO(img_bytes))
            image = image.convert("RGB")
            image = image.resize((128, 128), Image.LANCZOS)
            output = BytesIO()
            image.save(output, format='JPEG')
            return base64.b64encode(output.getvalue())
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
        ProductAttribute = self.env['product.attribute']
        ProductAttributeValue = self.env['product.attribute.value']
        Pricelist = self.env['product.pricelist']
        item_model = self.env['product.pricelist.item']

        for row in range(3, sheet.nrows):  # Empieza en la fila de los datos reales
            try:
                # ---- CATEGORÍA PERSONALIZADA ----
                metal = str(sheet.cell(row, 10).value).strip()
                prod_nac_imp = str(sheet.cell(row, 11).value).strip()
                taller_externa = str(sheet.cell(row, 12).value).strip()
                tipo_joya = str(sheet.cell(row, 14).value).strip()
                category_name = f"{metal} / {prod_nac_imp} / {taller_externa} / {tipo_joya}"

                categ = Category.search([('name', '=', category_name)], limit=1)
                if not categ:
                    categ = Category.create({'name': category_name})

                # ---- CAMPOS PRINCIPALES ----
                codigo = str(sheet.cell(row, 9).value).strip()         # default_code
                nombre = str(sheet.cell(row, 1).value).strip()         # Nombre
                modelo = str(sheet.cell(row, 2).value).strip()         # Modelo
                peso = self.safe_float(sheet.cell(row, 3).value)       # Peso
                costo = self.safe_float(sheet.cell(row, 4).value)      # Costo
                tarifa_publica = self.safe_float(sheet.cell(row, 5).value) # Tarifa Pública (precio venta)
                mayorista = self.safe_float(sheet.cell(row, 6).value)
                preferentes = self.safe_float(sheet.cell(row, 7).value)
                cod_barras = str(sheet.cell(row, 15).value).strip()    # CodBar
                imagen_url = str(sheet.cell(row, 16).value).strip()    # Imagen (URL)
                atributo = str(sheet.cell(row, 17).value).strip()      # Atributo (ej: Talla)
                valores_atributo = str(sheet.cell(row, 18).value).strip()  # Valores atributo

                # ---- DESCARGA Y REDIMENSIONA LA IMAGEN ----
                image_data = False
                if imagen_url and imagen_url.startswith('http'):
                    try:
                        resp = requests.get(imagen_url, timeout=10)
                        if resp.status_code == 200:
                            image_data = self.resize_image_128(resp.content)
                    except Exception:
                        image_data = False

                # ---- DUPLICADOS: NO crear si ya existe por código interno, nombre o código de barras ----
                duplicado = False
                if codigo and Product.search([('default_code', '=', codigo)], limit=1):
                    duplicado = True
                if nombre and Product.search([('name', '=', nombre)], limit=1):
                    duplicado = True
                if cod_barras and Product.search([('barcode', '=', cod_barras)], limit=1):
                    duplicado = True
                if duplicado:
                    continue  # Salta, ya existe por alguna clave única

                # ---- ATRIBUTOS Y VARIANTES ----
                attribute_line_ids = []
                if atributo and valores_atributo:
                    attr = ProductAttribute.search([('name', '=', atributo)], limit=1)
                    if not attr:
                        attr = ProductAttribute.create({'name': atributo})

                    valores_lista = [v.strip() for v in valores_atributo.split(',') if v.strip()]
                    value_ids = []
                    for valor in valores_lista:
                        value = ProductAttributeValue.search([('name', '=', valor), ('attribute_id', '=', attr.id)], limit=1)
                        if not value:
                            value = ProductAttributeValue.create({'name': valor, 'attribute_id': attr.id})
                        value_ids.append(value.id)
                    if value_ids:
                        attribute_line_ids.append((0, 0, {'attribute_id': attr.id, 'value_ids': [(6, 0, value_ids)]}))

                vals = {
                    'default_code': codigo,
                    'name': nombre,
                    'categ_id': categ.id,
                    'type': 'product',
                    'barcode': cod_barras,
                    'list_price': tarifa_publica,
                    'standard_price': costo,
                    'weight': peso,
                    'image_1920': image_data,
                    'attribute_line_ids': attribute_line_ids if attribute_line_ids else False,
                }
                if not vals['default_code'] or vals['default_code'] in ('', '0'):
                    vals['default_code'] = "CODE%05d" % (Product.search_count([]) + 1)
                product = Product.create(vals)

                # ---- PRECIOS POR LISTA (pricelists) ----
                pricelists = {
                    "Tarifa Pública": tarifa_publica,
                    "Mayorista": mayorista,
                    "Preferentes": preferentes,
                }

                currency_id = 2  # Ajusta según tu base

                for pricelist_name, price in pricelists.items():
                    if not price:
                        continue
                    pricelist = Pricelist.search([('name', '=', pricelist_name)], limit=1)
                    if not pricelist:
                        pricelist = Pricelist.create({'name': pricelist_name, 'currency_id': currency_id})
                    item_model.create({
                        'product_tmpl_id': product.id,
                        'pricelist_id': pricelist.id,
                        'fixed_price': price,
                        'min_quantity': 1,
                    })
            except Exception as e:
                # Log simple en consola de servidor o logging Odoo
                _logger = self.env['ir.logging']
                _logger.create({
                    'name': 'Import Products',
                    'type': 'server',
                    'level': 'info',
                    'message': f"Error al importar producto: {nombre} | Error: {e}",
                    'path': 'importar_productos_wizard',
                    'func': 'importar_productos',
                    'line': '0',
                })
                continue  # Siguiente producto