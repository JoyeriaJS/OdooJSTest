from odoo import models, fields, api

class RmaPosReportWizard(models.TransientModel):
    _name = 'rma.pos.report.wizard'
    _description = 'Reporte combinado RMA + POS'

    date_start = fields.Date(string='Fecha Inicio', required=True, default=fields.Date.context_today)
    date_end = fields.Date(string='Fecha Fin', required=True, default=fields.Date.context_today)

    def print_report(self):
        return self.env.ref('pos_qr_auth.ction_rma_pos_report_wizard"').report_action(self, data={
            'date_start': self.date_start,
            'date_end': self.date_end,
        })

    @api.model
    def _get_report_values(self, docids, data=None):
        wizard = self.browse(docids)[0]
        date_start = data.get('date_start')
        date_end = data.get('date_end')
        rmas = self.env['joyeria.reparacion'].search([
            ('fecha_retiro', '>=', date_start),
            ('fecha_retiro', '<=', date_end),
        ])
        poses = self.env['pos.order'].search([
            ('date_order', '>=', date_start),
            ('date_order', '<=', date_end),
        ])
        total_rma = sum(rma.amount_total for rma in rmas)
        total_pos = sum(pos.amount_total for pos in poses)
        return {
            'doc_ids': docids,
            'doc_model': 'rma.pos.report.wizard',
            'docs': wizard,
            'rmas': rmas,
            'poses': poses,
            'totals': {'rma': total_rma, 'pos': total_pos, 'grand': total_rma + total_pos},
            'data': data,
        }
