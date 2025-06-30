# -*- coding: utf-8 -*-
from odoo import models, api
from collections import defaultdict

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de Cargos entre Locales por Traspasos Internos'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].search([
            ('picking_type_code', '=', 'internal'),
            ('state', '=', 'done')
        ])

        data_by_month = defaultdict(list)

        for picking in pickings:
            month_key = picking.date_done.strftime('%B %Y') if picking.date_done else 'Sin Fecha'

            for move_line in picking.move_line_ids:
                if not move_line.product_id or move_line.qty_done <= 0:
                    continue

                price_unit = move_line.product_id.standard_price or 0.0
                subtotal = move_line.qty_done * price_unit

                data_by_month[month_key].append({
                    'origin': picking.location_id.display_name,
                    'destination': picking.location_dest_id.display_name,
                    'product': move_line.product_id.display_name,
                    'quantity': move_line.qty_done,
                    'price_unit': price_unit,
                    'subtotal': subtotal,
                })

        return {
            'months': [{'month': k, 'lines': v} for k, v in sorted(data_by_month.items())]
        }
