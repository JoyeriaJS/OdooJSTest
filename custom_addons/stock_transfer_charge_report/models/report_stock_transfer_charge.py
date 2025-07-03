from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte Simple de Traspasos con Precio Interno'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids) if docids else self.env['stock.picking'].search([])

        pricelist = self.env['product.pricelist'].search([('name', '=', 'Interno (CLP)')], limit=1)
        precios_interno = {}
        if pricelist:
            productos = pickings.mapped('move_line_ids_without_package.product_id')
            for producto in productos:
                item = self.env['product.pricelist.item'].search([
                    ('pricelist_id', '=', pricelist.id),
                    ('product_tmpl_id', '=', producto.product_tmpl_id.id),
                    ('applied_on', '=', '1_product')
                ], limit=1)
                precios_interno[producto.id] = item.fixed_price if item else 0.0
        else:
            productos = pickings.mapped('move_line_ids_without_package.product_id')
            for producto in productos:
                precios_interno[producto.id] = 0.0

        return {
            'docs': pickings,
            'precios_interno': precios_interno,  # <-- SIEMPRE mandamos este dict
        }
