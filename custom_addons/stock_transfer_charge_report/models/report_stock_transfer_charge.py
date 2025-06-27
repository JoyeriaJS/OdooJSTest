from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge.report_stock_transfer_charge'
    _description = 'Reporte de Cargos entre Locales por Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_end = fields.Date.context_today(self)
        date_start = date_end - relativedelta(months=12)
        pickings = self.env['stock.picking'].search([
            ('picking_type_code', '=', 'internal'),
            ('state', '=', 'done'),
            ('date_done', '>=', date_start),
            ('date_done', '<=', date_end),
        ])
        groups = {}
        for p in pickings:
            mes = p.date_done.strftime('%Y-%m')
            for move in p.move_lines:
                origin = p.location_id.display_name
                dest = p.location_dest_id.display_name
                product = move.product_id.display_name
                qty = move.quantity_done or 0.0
                price = move.product_id.standard_price or 0.0
                amount = qty * price
                key = (mes, origin, dest, product)
                groups.setdefault(key, {
                    'month': mes,
                    'origin': origin,
                    'destination': dest,
                    'product': product,
                    'amount': 0.0,
                })
                groups[key]['amount'] += amount

        lines = []
        for key, vals in sorted(groups.items()):
            year, month = vals['month'].split('-')
            month_name = datetime(int(year), int(month), 1).strftime('%B %Y')
            lines.append({
                'month_name': month_name,
                'origin': vals['origin'],
                'destination': vals['destination'],
                'product': vals['product'],
                'amount': vals['amount'],
            })
        return {
            'date_start': date_start,
            'date_end': date_end,
            'lines': lines,
        }