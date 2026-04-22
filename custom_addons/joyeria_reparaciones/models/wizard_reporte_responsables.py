from odoo import models, fields, api
from datetime import datetime

class WizardReporteResponsables(models.TransientModel):
    _name = 'wizard.reporte.responsables'
    _description = 'Asistente para generar reporte por responsables'

    fecha_inicio = fields.Date(string="Fecha desde", required=True)
    fecha_fin = fields.Date(string="Fecha hasta", required=True)
    responsable_id = fields.Many2one('res.users', string="Responsable", required=False)

    def generar_reporte(self):
        domain = [('fecha_entrega', '>=', self.fecha_inicio), ('fecha_entrega', '<=', self.fecha_fin)]
        if self.responsable_id:
            domain.append(('responsable_id', '=', self.responsable_id.id))

        reparaciones = self.env['joyeria.reparacion'].search(domain, order='fecha_entrega asc')

        return self.env.ref('joyeria_reparaciones.reporte_reparaciones_responsable_action').report_action(
            reparaciones,
            data={
                'fecha_inicio': self.fecha_inicio.strftime('%Y-%m-%d'),
                'fecha_fin': self.fecha_fin.strftime('%Y-%m-%d'),
            }
        )