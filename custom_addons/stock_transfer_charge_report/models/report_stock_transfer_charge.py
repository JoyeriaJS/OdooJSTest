from odoo import models, api
from collections import defaultdict

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte General de Traspasos entre Locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].search([
            ('picking_type_code', '=', 'internal'),
        ], order='date_done desc')

        transfers = []
        for picking in pickings:
            for move in picking.move_ids:
                product = move.product_id
                transfers.append({
                    'date': picking.date_done or picking.scheduled_date or picking.date,
                    'state': picking.state,
                    'origin': picking.location_id.display_name,
                    'destination': picking.location_dest_id.display_name,
                    'product': product.display_name,
                    'quantity': move.product_uom_qty,
                    'price_unit': product.standard_price,
                    'subtotal': move.product_uom_qty * (product.standard_price or 0.0),
                })

        return {
            'transfers': transfers
        }
