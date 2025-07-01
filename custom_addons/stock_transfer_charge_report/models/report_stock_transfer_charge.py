from odoo import models, api
from collections import defaultdict

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte General de Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Trae todos los pickings (traspasos) de cualquier tipo/estado
        pickings = self.env['stock.picking'].search([], order="date_done desc")

        data_by_month = defaultdict(list)

        for picking in pickings:
            date = picking.date_done or picking.scheduled_date or picking.date or False
            month_key = date.strftime('%B %Y') if date else 'Sin Fecha'
            for line in picking.move_line_ids:
                product = line.product_id
                quantity = line.qty_done or 0.0
                price = product.standard_price or 0.0
                subtotal = quantity * price
                data_by_month[month_key].append({
                    'name': picking.name,
                    'origin': picking.location_id.display_name,
                    'destination': picking.location_dest_id.display_name,
                    'product': product.display_name,
                    'quantity': quantity,
                    'price_unit': price,
                    'subtotal': subtotal,
                    'state': picking.state,
                    'type': picking.picking_type_id.name if picking.picking_type_id else 'N/A',
                })

        return {
            'months': [{'month': m, 'lines': l} for m, l in data_by_month.items()],
        }
