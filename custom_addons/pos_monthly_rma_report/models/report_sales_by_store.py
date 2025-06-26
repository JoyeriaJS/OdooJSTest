# -*- coding: utf-8 -*-
from odoo import api, models, fields
import datetime

class ReportSalesByStore(models.AbstractModel):
    _name = 'report.pos_monthly_rma_report.report_sales_by_store_template'
    _description = 'Reporte Mensual RMA + POS'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Current month
        today = fields.Date.context_today(self)
        date_start = today.replace(day=1)
        date_end = today
        # Aggregate RMA
        rmas = self.env['joyeria.reparacion'].search([
            ('fecha_firma', '>=', date_start),
            ('fecha_firma', '<=', date_end)
        ])
        rma_total = sum(r.saldo or 0.0 for r in rmas)
        # Aggregate POS
        pos_orders = self.env['pos.order'].search([
            ('date_order', '>=', date_start),
            ('date_order', '<=', date_end)
        ])
        pos_total = sum(o.amount_total or 0.0 for o in pos_orders)
        # Single group for the month
        month_label = date_start.strftime('%B %Y')
        groups = [{
            'date': month_label,
            'rma_total': rma_total,
            'pos_total': pos_total,
            'grand_total': rma_total + pos_total
        }]
        return {
            'doc_ids': docids,
            'doc_model': '',
            'data': {'date_start': date_start, 'date_end': date_end},
            'groups': groups,
        }
