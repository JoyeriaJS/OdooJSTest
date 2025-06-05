from odoo import models, fields, api

class ReporteResponsablesWizard(models.TransientModel):
    _name = "reporte.responsables.wizard"
    _description = "Wizard para reporte de responsables"

    responsable_id = fields.Many2one('res.users', string='Responsable', required=True)
    fecha_inicio = fields.Date(string='Fecha inicio', required=True)
    fecha_fin = fields.Date(string='Fecha fin', required=True)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_id = self.env.context.get('active_id')
        if active_id:
            res['responsable_id'] = active_id
        return res

    def imprimir_reporte(self):
        data = {
            'responsable_id': self.responsable_id.id,
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
        }
        return self.env.ref('reporte_responsables_wizard.action_reporte_responsables_pdf').report_action(self, data=data)
