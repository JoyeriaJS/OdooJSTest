# -*- coding: utf-8 -*-
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
            ('state', '=', 'done'),
            ('date_done', '!=', False)
        ])

        data_by_month = defaultdict(list)

        for p in pickings:
            date = p.date_done
            month_key = date.strftime('%Y-%m')  # Ej: "2025-06"
            for move in p.move_lines:
                qty = move.quantity_done or 0.0
                price = move.product_id.standard_price or 0.0
                amount = qty * price
                if qty == 0:
                    continue
                data_by_month[month_key].append({
                    'origin': p.location_id.display_name,
                    'destination': p.location_dest_id.display_name,
                    'product': move.product_id.display_name,
                    'quantity': qty,
                    'price': price,
                    'total': amount,
                })

        return {
            'data_by_month': dict(data_by_month),
        }
