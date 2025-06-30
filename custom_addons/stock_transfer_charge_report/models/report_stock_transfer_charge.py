# -*- coding: utf-8 -*-
from odoo import models, api
from collections import defaultdict

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de Cargos entre Locales por Traspasos Internos'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Buscar traslados internos que estén en estado 'done'
        pickings = self.env['stock.picking'].search([
            ('picking_type_code', '=', 'internal'),
            ('state', '=', 'done'),
        ])

        data_by_month = defaultdict(list)

        for picking in pickings:
            if not picking.move_lines:
                continue

            if not picking.date_done:
                continue  # ignorar sin fecha efectiva

            month_key = picking.date_done.strftime('%B %Y')

            for move in picking.move_lines:
                product = move.product_id
                qty = move.quantity_done
                price = product.standard_price or 0.0
                subtotal = qty * price

                data_by_month[month_key].append({
                    'origin': picking.location_id.display_name,
                    'destination': picking.location_dest_id.display_name,
                    'product': product.display_name,
                    'quantity': qty,
                    'price_unit': price,
                    'subtotal': subtotal,
                })

        return {
            'months': [{'month': m, 'lines': lines} for m, lines in sorted(data_by_month.items())],
        }
