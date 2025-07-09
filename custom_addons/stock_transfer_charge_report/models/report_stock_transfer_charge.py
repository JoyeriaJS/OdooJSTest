from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge'        # ← nombre corto
    _description = 'Reporte Simple de Traspasos'
    _auto = False    

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids) if docids else self.env['stock.picking'].search([])
        movimientos = []

        for picking in pickings:
            for ml in picking.move_line_ids_without_package:
                movimientos.append({
                    'code': ml.product_id.default_code or '',
                    'name': ml.product_id.display_name or '',
                    'qty': ml.quantity or 0.0,
                    'uom': ml.product_uom_id.name or '',
                    'origen': picking.location_id.display_name or '',
                    'destino': picking.location_dest_id.display_name or '',
                    'picking_name': picking.name or '',
                    'fecha': picking.date_done.strftime('%d/%m/%Y %H:%M:%S') if picking.date_done else '',
                    'estado': picking.state or '',
                })

        return {
            'movimientos': movimientos,
            'pickings': pickings,
            
        }
