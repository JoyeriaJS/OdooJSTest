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
        data = {
            'date_start': self.date_start.strftime('%Y-%m-%d'),
            'date_stop': self.date_stop.strftime('%Y-%m-%d'),
            'session_id': self.session_id.id,
        }
        return {
            'type': 'ir.actions.report',
            'report_type': 'qweb-pdf',
            'report_name': 'pos_daily_rma_report.action_report_pos_daily_rma',
            'data': data,
            'context': dict(self.env.context),
        }
