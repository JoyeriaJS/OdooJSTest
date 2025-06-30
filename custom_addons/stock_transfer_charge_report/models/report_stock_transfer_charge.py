from odoo import models, api
from collections import defaultdict

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de Cargos entre Locales por Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].search([
            ('picking_type_code', '=', 'internal'),
            ('state', '=', 'done'),
            ('date_done', '!=', False)
        ])

        data_by_month = defaultdict(list)

        for picking in pickings:
            for move in picking.move_lines:
                qty = move.quantity_done or 0.0
                price = move.product_id.standard_price or 0.0
                if qty <= 0.0 or price <= 0.0:
                    continue
                month_key = picking.date_done.strftime('%B %Y')
                data_by_month[month_key].append({
                    'origin': picking.location_id.display_name,
                    'destination': picking.location_dest_id.display_name,
                    'product': move.product_id.display_name,
                    'quantity': qty,
                    'price_unit': round(price, 2),
                    'subtotal': round(qty * price, 2),
                })

        return {
            'months': [{'month': m, 'lines': lines} for m, lines in sorted(data_by_month.items())]
        }
