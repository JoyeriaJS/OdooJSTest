from odoo import models
from datetime import timedelta
from odoo.fields import Date

class VendorAnalyzer(models.Model):
    _name = 'ai.vendor.analyzer'
    _description = 'Vendor Analyzer'

    def analyze(self):

        today = Date.today()
        last_week = today - timedelta(days=7)

        orders = self.env['pos.order'].search([
            ('date_order', '>=', last_week),
            ('state', '=', 'paid')
        ])

        vendor_totals = {}

        for order in orders:
            user = order.user_id.name
            vendor_totals[user] = vendor_totals.get(user, 0) + order.amount_total

        return vendor_totals
