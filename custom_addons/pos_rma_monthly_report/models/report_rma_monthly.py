# -*- coding: utf-8 -*-
from odoo import api, models, fields
from collections import OrderedDict

class ReportRmaMonthly(models.AbstractModel):
    _name = 'report.pos_rma_monthly_report.template_rma_monthly'
    _description = 'Reporte Mensual RMA + POS'

    @api.model
    def _get_report_values(self, docids, data=None):
        today = fields.Date.context_today(self)
        start = today.replace(day=1)
        rmas = self.env['joyeria.reparacion'].search([
            ('fecha_recepcion', '>=', start),
            ('fecha_recepcion', '<=', today),
        ])
        poses = self.env['pos.order'].search([
            ('date_order', '>=', f"{start} 00:00:00"),
            ('date_order', '<=', f"{today} 23:59:59"),
        ])
        groups = OrderedDict()
        for r in rmas:
            d = r.fecha_recepcion[:10]
            groups.setdefault(d, {'date': d, 'rma': 0.0, 'pos': 0.0})
            groups[d]['rma'] += r.subtotal or 0.0
        for p in poses:
            d = p.date_order[:10]
            groups.setdefault(d, {'date': d, 'rma': 0.0, 'pos': 0.0})
            groups[d]['pos'] += p.amount_total or 0.0
        sorted_data = [groups[d] for d in sorted(groups)]
        return {
            'doc_ids': docids,
            'doc_model': 'joyeria.reparacion',
            'date_start': start,
            'date_stop': today,
            'groups': sorted_data,
        }
