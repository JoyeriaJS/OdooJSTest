from odoo import models, api
from collections import defaultdict
from datetime import datetime

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte mensual de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].search([
            ('picking_type_code', '=', 'internal'),
            ('state', '=', 'done'),
            ('date_done', '!=', False),
        ])

        data_by_month = defaultdict(list)

        for picking in pickings:
            date_done = picking.date_done
            mes = date_done.strftime('%Y-%m')

            for move in picking.move_ids_without_package:
                price = move.product_id.standard_price or 0.0
                qty = move.quantity_done or 0.0
                total = price * qty

                data_by_month[mes].append({
                    'date': date_done.strftime('%d/%m/%Y'),
                    'origin': picking.location_id.display_name,
                    'destination': picking.location_dest_id.display_name,
                    'product': move.product_id.display_name,
                    'quantity': qty,
                    'price': price,
                    'total': total,
                })

        # 🔥 Esto asegura que el template reciba la variable que busca
        return {
            'doc_ids': docids,
            'doc_model': 'stock.picking',
            'data_by_month': dict(data_by_month),
        }
