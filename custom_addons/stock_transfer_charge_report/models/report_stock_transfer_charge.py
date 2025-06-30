from odoo import models, api
from collections import defaultdict

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
            if not picking.move_line_ids:
                continue
            for ml in picking.move_line_ids:
                if not ml.product_id or not ml.quantity_done:
                    continue
                month_key = picking.date_done.strftime('%B %Y') if picking.date_done else 'Sin Fecha'
                data_by_month[month_key].append({
                    'origin': ml.location_id.display_name,
                    'destination': ml.location_dest_id.display_name,
                    'product': ml.product_id.display_name,
                    'quantity': ml.quantity_done,
                    'price_unit': ml.product_id.standard_price,
                    'subtotal': ml.quantity_done * ml.product_id.standard_price
                })

        return {
            'months': [{'month': m, 'lines': lines} for m, lines in data_by_month.items()]
        }
