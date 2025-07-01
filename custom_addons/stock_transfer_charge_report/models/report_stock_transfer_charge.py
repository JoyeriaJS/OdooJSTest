from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte General de Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Buscar todos los pickings (sin filtro, para probar)
        pickings = self.env['stock.picking'].search([])
        lines = []
        for picking in pickings:
            for move in picking.move_ids:  # stock.move, NO move_line_ids
                lines.append({
                    'picking_name': picking.name,
                    'origin': picking.location_id.display_name,
                    'destination': picking.location_dest_id.display_name,
                    'product': move.product_id.display_name,
                    'quantity': move.product_uom_qty,
                    'price_unit': move.product_id.standard_price,
                    'subtotal': move.product_uom_qty * (move.product_id.standard_price or 0.0),
                    'state': picking.state,
                    'type': picking.picking_type_code,
                })
        # Si quieres ver por consola lo que obtiene:
        # import logging; logging.getLogger('odoo').info(lines)
        return {'lines': lines}
