from odoo import models, api
from collections import defaultdict
from datetime import datetime

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de Cargos entre Locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        data_by_month = defaultdict(list)

        pickings = self.env['stock.picking'].search([
            ('picking_type_code', '=', 'internal'),
            ('state', '=', 'done'),
            ('date_done', '!=', False),
        ])

        for picking in pickings:
            date_done = picking.date_done
            month = date_done.strftime('%Y-%m')

            for move in picking.move_ids_without_package:
                price = move.product_id.standard_price or 0.0
                qty = move.quantity_done or 0.0
                total = qty * price

                data_by_month[month].append({
                    'date': date_done.strftime('%d/%m/%Y'),
                    'origin': picking.location_id.display_name,
                    'destination': picking.location_dest_id.display_name,
                    'product': move.product_id.display_name,
                    'quantity': qty,
                    'price': price,
                    'total': total,
                })

        return {
            'data_by_month': dict(data_by_month),  # 👈🏼 ESTA VARIABLE ES LA CLAVE
        }
