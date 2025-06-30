# report_stock_transfer_charge.py
from odoo import models, api
from collections import defaultdict
from datetime import datetime

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de Cargos entre Locales por Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].search([
            ('picking_type_code', '=', 'internal'),
            ('state', '=', 'done')
        ])

        data_by_month = defaultdict(list)

        for picking in pickings:
            if not picking.move_lines:
                continue
            month_key = picking.date_done.strftime('%B %Y') if picking.date_done else 'Sin Fecha'
            for move in picking.move_lines:
                line = {
                    'origin': picking.location_id.display_name,
                    'destination': picking.location_dest_id.display_name,
                    'product': move.product_id.display_name,
                    'quantity': move.quantity_done,
                    'price_unit': move.product_id.standard_price,
                    'subtotal': move.quantity_done * move.product_id.standard_price
                }
                data_by_month[month_key].append(line)

        return {
            'months': [{'month': m, 'lines': lines} for m, lines in data_by_month.items()]
        }
