from odoo import models, fields, api
from collections import defaultdict
from datetime import datetime

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de cargos entre locales agrupado por mes'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].search([
            ('picking_type_code', '=', 'internal'),
            ('state', '=', 'done'),
        ])

        data_by_month = defaultdict(list)
        for picking in pickings:
            date = picking.date_done
            if not date:
                continue
            month_key = date.strftime('%Y-%m')
            for move in picking.move_ids_without_package:
                data_by_month[month_key].append({
                    'date': date.strftime('%d/%m/%Y'),
                    'origin': picking.location_id.display_name,
                    'destination': picking.location_dest_id.display_name,
                    'product': move.product_id.display_name,
                    'quantity': move.quantity_done,
                    'price': move.product_id.standard_price,
                    'total': move.quantity_done * move.product_id.standard_price,
                })

        # Ordenamos por mes
        sorted_data = dict(sorted(data_by_month.items()))
        return {
            'data_by_month': sorted_data,
        }
