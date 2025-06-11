from odoo import models, fields, api
from datetime import datetime

class ReporteSalidaTaller(models.TransientModel):
    _name = 'joyeria.salida_taller'
    _description = 'Wizard para reporte de salida mensual'

    mes = fields.Selection([
        ('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'),
        ('4', 'Abril'), ('5', 'Mayo'), ('6', 'Junio'),
        ('7', 'Julio'), ('8', 'Agosto'), ('9', 'Septiembre'),
        ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')
    ], string='Mes', required=True)

    def imprimir_pdf(self):
        return self.env.ref('joyeria_reporte_salida_taller_funcional_final_corregido.reporte_salida_taller_pdf_action').report_action(self)