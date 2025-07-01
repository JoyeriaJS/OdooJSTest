from odoo import api, models
from collections import defaultdict

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de Cargos entre Locales por Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].search([
            ('picking_type_code', '=', 'internal'),
            ('state', '=', 'done'),
        ])
        data_by_month = defaultdict(list)
        for picking in pickings:
            month = picking.date_done.strftime('%B %Y') if picking.date_done else 'Sin Fecha'
            for line in picking.move_line_ids.filtered(lambda l: l.qty_done):
                price = line.product_id.standard_price or 0.0
                qty   = line.qty_done
                data_by_month[month].append({
                    'origin':      picking.location_id.display_name,
                    'destination': picking.location_dest_id.display_name,
                    'product':     line.product_id.display_name,
                    'quantity':    qty,
                    'price_unit':  price,
                    'subtotal':    qty * price,
                })
        return {
            'months': [{'month': m, 'lines': l} for m, l in data_by_month.items()],
        }
