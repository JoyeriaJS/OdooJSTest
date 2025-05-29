from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import io
import csv

class CargarCSVWizard(models.TransientModel):
    _name = 'wizard.cargar.csv'
    _description = 'Wizard para Cargar Productos desde CSV'

    archivo_csv = fields.Binary("Archivo CSV", required=True)
    nombre_archivo = fields.Char("Nombre del Archivo")

    def cargar_productos(self):
        if not self.archivo_csv:
            raise UserError(_("Debe subir un archivo CSV."))

        data = base64.b64decode(self.archivo_csv)
        archivo = io.StringIO(data.decode('utf-8'))
        reader = csv.DictReader(archivo)
        for row in reader:
            self.env['joyeria.inventario'].create({
                'name': row.get('name', 'Producto sin nombre'),
                'sucursal': row.get('sucursal', ''),
                'tipo': row.get('tipo', 'recepcion'),
                'estado': row.get('estado', 'a_procesar'),
                'cantidad': int(row.get('cantidad', 0)),
                'precio_compra': float(row.get('precio_compra', 0.0)),
                'precio_sugerido': float(row.get('precio_sugerido', 0.0)),
                'descripcion': row.get('descripcion', ''),
                # 'foto': ...  # solo si tienes base64
            })
