# -*- coding: utf-8 -*-
from odoo import models, fields

class PosDailyRmaReportWizard(models.TransientModel):
    _name = 'pos.daily.rma.report.wizard'
    _description = 'Reporte Diario de POS y RMA'

    date_start = fields.Date(
        string='Fecha Inicio', required=True,
        default=lambda self: fields.Date.context_today(self)
    )
    date_stop = fields.Date(
        string='Fecha Fin', required=True,
        default=lambda self: fields.Date.context_today(self)
    )
    session_id = fields.Many2one(
        'pos.session', string='Sesión POS', required=True,
        default=lambda self: self.env['pos.session']
            .search([('state', '!=', 'closed')], limit=1)
    )

    def generate_report(self):
        # Busca el reporte por report_name
        report = self.env['ir.actions.report'].search([
            ('report_name', '=', 'pos_daily_rma_report.template_pos_daily_rma')
        ], limit=1)
        return report.report_action(self, data={
            'date_start': self.date_start,
            'date_stop': self.date_stop,
            'session_id': self.session_id.id,
        })
