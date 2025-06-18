# -*- coding: utf-8 -*-
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

        duplicates = []      # guardaremos los códigos o nombres duplicados
        imported_count = 0   # contador de productos creados

        for row in range(3, sheet.nrows):  # comienza en fila 3
            # Lectura básica de celdas (ajusta índices según tu Excel)
            codigo = str(sheet.cell(row, 9).value).strip()
            nombre = str(sheet.cell(row, 1).value).strip()
            modelo = str(sheet.cell(row, 2).value).strip()
            peso = self.safe_float(sheet.cell(row, 3).value)
            costo = self.safe_float(sheet.cell(row, 4).value)
            tarifa_publica = self.safe_float(sheet.cell(row, 5).value)
            cod_barras = str(sheet.cell(row, 15).value).strip()
            imagen_url = str(sheet.cell(row, 16).value).strip()
            atributo = str(sheet.cell(row, 17).value).strip()
            valores_atributo = str(sheet.cell(row, 18).value).strip()

            # Categoría compuesta
            metal = str(sheet.cell(row, 10).value).strip()
            prod_nac_imp = str(sheet.cell(row, 11).value).strip()
            taller_externa = str(sheet.cell(row, 12).value).strip()
            tipo_joya = str(sheet.cell(row, 14).value).strip()
            category_name = f"{metal} / {prod_nac_imp} / {taller_externa} / {tipo_joya}"
            categ = Category.search([('name', '=', category_name)], limit=1)
            if not categ:
                categ = Category.create({'name': category_name})

            # Descarga y redimensiona imagen si hay URL
            image_data = False
            if imagen_url.startswith('http'):
                try:
                    resp = requests.get(imagen_url, timeout=10)
                    if resp.status_code == 200:
                        image_data = self.resize_image_128(resp.content)
                except Exception:
                    image_data = False

            # Detección de duplicados por código
            if codigo:
                if Product.search([('default_code', '=', codigo)], limit=1):
                    duplicates.append(codigo)
                    continue

            # Detección de duplicados por nombre
            if nombre:
                if Product.search([('name', '=', nombre)], limit=1):
                    duplicates.append(nombre)
                    continue

            # Preparar atributos si aplica
            attribute_line_ids = []
            if atributo and valores_atributo:
                attr = ProductAttribute.search([('name', '=', atributo)], limit=1)
                if not attr:
                    attr = ProductAttribute.create({'name': atributo})
                vals_list = [v.strip() for v in valores_atributo.split(',') if v.strip()]
                value_ids = []
                for v in vals_list:
                    val = ProductAttributeValue.search([
                        ('name', '=', v), ('attribute_id', '=', attr.id)
                    ], limit=1)
                    if not val:
                        val = ProductAttributeValue.create({
                            'name': v, 'attribute_id': attr.id
                        })
                    value_ids.append(val.id)
                if value_ids:
                    attribute_line_ids = [(0, 0, {
                        'attribute_id': attr.id,
                        'value_ids': [(6, 0, value_ids)]
                    })]

            # Datos del producto
            prod_vals = {
                'default_code': codigo or f"CODE%05d" % (Product.search_count([]) + 1),
                'name': nombre,
                'categ_id': categ.id,
                'type': 'product',
                'barcode': cod_barras,
                'list_price': tarifa_publica,
                'standard_price': costo,
                'weight': peso,
                'image_1920': image_data,
                'attribute_line_ids': attribute_line_ids or False,
            }
            Product.create(prod_vals)
            imported_count += 1

        # Construir mensaje de resultado
        msg = f"Importación finalizada: {imported_count} productos nuevos."
        if duplicates:
            uniques = list(dict.fromkeys(duplicates))
            msg += f" Se omitieron {len(uniques)} duplicados: {', '.join(uniques)}."

        # Devolver acción cliente para mostrar notificación
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': "Importar Productos",
                'message': msg,
                'sticky': False,
            }
        }
