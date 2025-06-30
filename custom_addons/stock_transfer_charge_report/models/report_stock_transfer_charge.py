from odoo import models, fields, api
from collections import defaultdict
from datetime import datetime

class ReportMonthlyTransferCharges(models.AbstractModel):
    _name = 'report.stock.report_monthly_transfer_charges_template'
    _description = 'Reporte mensual de cargos entre locales por traspasos internos'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].search([
            ('picking_type_code', '=', 'internal'),
            ('state', '=', 'done')
        ])

        grouped = {}
        for picking in pickings:
            date = picking.date_done.date() if picking.date_done else None
            if not date:
                continue
            year_month = date.strftime('%Y-%m')

            for move in picking.move_lines:
                qty = move.quantity_done or 0.0
                price = move.product_id.standard_price or 0.0
                amount = qty * price

                origin = picking.location_id.display_name
                destination = picking.location_dest_id.display_name
                product_name = move.product_id.display_name

                grouped.setdefault(year_month, [])
                grouped[year_month].append({
                    'origin': origin,
                    'destination': destination,
                    'product': product_name,
                    'amount': amount,
                    'qty': qty,
                    'unit_price': price,
                    'date': date.strftime('%d/%m/%Y'),
                })

        return {
            'data_by_month': grouped
        }
