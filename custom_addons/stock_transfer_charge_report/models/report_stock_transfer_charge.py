from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de Cargos entre Locales por Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Si docids está vacío, trae todos los pickings (para prueba)
        if not docids:
            pickings = self.env['stock.picking'].search([])
        else:
            pickings = self.env['stock.picking'].browse(docids)
        
        lines = []
        for picking in pickings:
            for move in picking.move_ids:
                lines.append({
                    'picking_name': picking.name or '',
                    'origin': picking.location_id.display_name or '',
                    'destination': picking.location_dest_id.display_name or '',
                    'product': move.product_id.display_name or '',
                    'quantity': move.product_uom_qty or 0,
                    'price_unit': move.product_id.standard_price or 0,
                    'subtotal': (move.product_uom_qty or 0) * (move.product_id.standard_price or 0),
                    'state': picking.state or '',
                    'type': picking.picking_type_id.name or '',
                })

        return {
            'lines': lines,
            'test_text': f'IDs recibidos: {docids} - total traspasos: {len(lines)}'
        }
