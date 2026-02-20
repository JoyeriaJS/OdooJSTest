from odoo import models
from datetime import timedelta
from odoo.fields import Date

class SalesAnalyzer(models.Model):
    _name = 'ai.sales.analyzer'
    _description = 'Sales Analyzer'

    def analyze(self):

        today = Date.today()
        last_week = today - timedelta(days=7)
        prev_week = today - timedelta(days=14)

        # Estados válidos en POS Odoo 17
        valid_states = ['paid', 'done', 'invoiced']

        orders_last_week = self.env['pos.order'].search([
            ('date_order', '>=', last_week),
            ('date_order', '<=', today),
            ('state', 'in', valid_states)
        ])

        orders_prev_week = self.env['pos.order'].search([
            ('date_order', '>=', prev_week),
            ('date_order', '<', last_week),
            ('state', 'in', valid_states)
        ])

        total_last = sum(orders_last_week.mapped('amount_total'))
        total_prev = sum(orders_prev_week.mapped('amount_total'))

        variation = 0
        if total_prev > 0:
            variation = ((total_last - total_prev) / total_prev) * 100

        return {
            'total_last_week': total_last,
            'total_prev_week': total_prev,
            'variation': variation,
            'orders_count_last_week': len(orders_last_week),
            'orders_count_prev_week': len(orders_prev_week),
        }