from odoo import models, api
from collections import defaultdict
from datetime import datetime

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de Cargos entre Locales por Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Elimina filtros para forzar que entregue todo
        pickings = self.env['stock.picking'].search([
            ('picking_type_code', '=', 'internal'),
        ])

        data_by_month = defaultdict(list)

        for picking in pickings:
            # Usamos move_line_ids, no move_lines
            for line in picking.move_line_ids:
                product = line.product_id
                quantity = line.qty_done or 0.0
                price = product.standard_price or 0.0
                subtotal = quantity * price
                date = picking.date_done or picking.scheduled_date or picking.date or datetime.now()
                month_key = date.strftime('%B %Y')
                data_by_month[month_key].append({
                    'origin': picking.location_id.display_name,
                    'destination': picking.location_dest_id.display_name,
                    'product': product.display_name,
                    'quantity': quantity,
                    'price_unit': price,
                    'subtotal': subtotal,
                })

        return {
            'months': [{'month': m, 'lines': l} for m, l in data_by_month.items()],
        }

