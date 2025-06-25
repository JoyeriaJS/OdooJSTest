# -*- coding: utf-8 -*-
from odoo import api, models, fields
from collections import OrderedDict

class ReportRmaMonthly(models.AbstractModel):
    _name = 'report.pos_monthly_rma_report_fixed2.rma_monthly_template'
    _description = 'Reporte Mensual RMA + POS'

    @api.model
    def _get_report_values(self, docids, data=None):
        today = fields.Date.context_today(self)
        start = today.replace(day=1)
        # Fetch RMA and POS orders
        rmas = self.env['joyeria.reparacion'].search([
            ('fecha_recepcion', '>=', start),
            ('fecha_recepcion', '<=', today),
        ])
        pos_orders = self.env['pos.order'].search([
            ('date_order', '>=', f"{start} 00:00:00"),
            ('date_order', '<=', f"{today} 23:59:59"),
        ])
        # Group by date
        groups = OrderedDict()
        for r in rmas:
            try:
                d = r.fecha_recepcion.strftime('%Y-%m-%d')
            except:
                d = str(r.fecha_recepcion)[:10]
            groups.setdefault(d, {'date': d, 'rma_total': 0.0, 'pos_total': 0.0})
            groups[d]['rma_total'] += r.subtotal or 0.0
        for p in pos_orders:
            try:
                d = p.date_order.strftime('%Y-%m-%d')
            except:
                d = str(p.date_order)[:10]
            groups.setdefault(d, {'date': d, 'rma_total': 0.0, 'pos_total': 0.0})
            groups[d]['pos_total'] += p.amount_total or 0.0
        sorted_groups = [groups[k] for k in sorted(groups)]
        return {
            'doc_ids': docids,
            'doc_model': 'joyeria.reparacion',
            'date_start': start,
            'date_end': today,
            'groups': sorted_groups,
        }
