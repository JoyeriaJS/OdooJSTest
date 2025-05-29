from odoo import models, fields, api
import base64
import io
import pandas as pd

class CargarExcelProductos(models.TransientModel):
    _name = 'wizard.cargar.excel'
    _description = 'Wizard para Cargar Productos desde Excel'

    archivo_excel = fields.Binary(string="Archivo Excel", required=True)
    nombre_archivo = fields.Char("Nombre del Archivo")

    def generar_codigo_personalizado(self, row):
        # Ejemplo de generación, reemplaza con lógica real de tablas
        return f"{row['Modelo']}-{row['Color']}-{row['Material']}"

    def cargar_productos(self):
        if not self.archivo_excel:
            raise UserError("Debe cargar un archivo Excel válido.")

        datos = base64.b64decode(self.archivo_excel)
        archivo = io.BytesIO(datos)

        df = pd.read_excel(archivo, sheet_name="Productos")

        for index, row in df.iterrows():
            codigo = self.generar_codigo_personalizado(row)

            self.env['joyeria.inventario'].create({
                'name': row.get('Nombre', 'Producto sin nombre'),
                'sucursal': row.get('Sucursal', ''),
                'tipo': row.get('Tipo', 'recepcion'),
                'estado': row.get('Estado', 'a_procesar'),
                'cantidad': row.get('Cantidad', 0),
                'codigo': codigo,
                'precio_compra': row.get('Precio Compra', 0.0),
                'precio_sugerido': row.get('Precio Sugerido', 0.0),
                'descripcion': row.get('Descripción', ''),
                # 'foto': base64_image si llega la imagen como base64 o desde archivo externo
            })
