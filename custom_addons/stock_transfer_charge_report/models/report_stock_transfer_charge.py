from odoo import models, api

class ReportPickingTransfer(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte personalizado de traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Solo los docids seleccionados
        pickings = self.env['stock.picking'].browse(docids)
        lines = []
        for picking in pickings:
            for move in picking.move_ids_without_package:
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
        return {
            'lines': lines,
            'test_text': "ESTE ES EL REPORTE DE TRASPASOS"  # Solo para probar
        }
