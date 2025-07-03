from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte Simple de Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids) if docids else self.env['stock.picking'].search([])
        movimientos = []
        pricelist = self.env['product.pricelist'].search([('name', 'ilike', 'Interno')], limit=1)
        for picking in pickings:
            for ml in picking.move_line_ids_without_package:
                precio_interno = 0.0
                if pricelist:
                    item = self.env['product.pricelist.item'].search([
                        ('pricelist_id', '=', pricelist.id),
                        ('product_tmpl_id', '=', ml.product_id.product_tmpl_id.id),
                        ('applied_on', '=', '1_product'),
                    ], limit=1)
                    if item:
                        precio_interno = item.fixed_price
                subtotal = ml.quantity * precio_interno
                movimientos.append({
                    'producto': ml.product_id.display_name or '',
                    'cantidad': ml.quantity or 0.0,
                    'uom': ml.product_uom_id.name or '',
                    'precio_interno': precio_interno,
                    'subtotal_interno': subtotal,
                    'origen': picking.location_id.display_name or '',
                    'destino': picking.location_dest_id.display_name or '',
                    'traspaso': picking.name or '',
                    'fecha': picking.date_done.strftime('%d/%m/%Y %H:%M:%S') if picking.date_done else '',
                    'estado': picking.state or '',
                })
        return {
            'movimientos': movimientos,
        }
