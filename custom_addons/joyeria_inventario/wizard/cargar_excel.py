from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import io
import pandas as pd

class CargarExcelWizard(models.TransientModel):
    _name = 'wizard.cargar.excel'
    _description = 'Wizard para Cargar Productos desde Excel'

    archivo_excel = fields.Binary(string="Archivo Excel", required=True)
    nombre_archivo = fields.Char(string="Nombre del Archivo")

    def cargar_productos(self):
        if not self.archivo_excel:
            raise UserError(_("Debe cargar un archivo Excel válido."))

        data = base64.b64decode(self.archivo_excel)
        archivo = io.BytesIO(data)
        df = pd.read_excel(archivo, sheet_name="Productos")

        for i, row in df.iterrows():
            self.env['joyeria.inventario'].create({
                'name': row.get('Nombre', 'Producto sin nombre'),
                'codigo': row.get('CodJS+SigItem', ''),
                'precio_compra': row.get('Costo', 0.0),
                'precio_sugerido': row.get('Tarifa Pública', 0.0),
                'descripcion': f"Modelo: {row.get('Modelo', '')}, Peso: {row.get('Peso', '')}",
                'cantidad': 1,
                'tipo': 'recepcion',
                'estado': 'a_procesar',
            })
