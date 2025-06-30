from odoo import models, api
from collections import defaultdict
from datetime import datetime

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].search([
            ('picking_type_code', '=', 'internal'),
            ('state', '=', 'done'),
            ('date_done', '!=', False),
        ])

        grouped = defaultdict(list)

        for picking in pickings:
            fecha = picking.date_done
            year_month = fecha.strftime('%Y-%m')

            for move in picking.move_lines:
                qty = move.quantity_done or 0.0
                price = move.product_id.standard_price or 0.0
                total = qty * price

                grouped[year_month].append({
                    'date': fecha.strftime('%d/%m/%Y'),
                    'origin': picking.location_id.display_name,
                    'destination': picking.location_dest_id.display_name,
                    'product': move.product_id.display_name,
                    'qty': qty,
                    'unit_price': price,
                    'total': total,
                })

        return {
            'data_by_month': dict(grouped),
        }
