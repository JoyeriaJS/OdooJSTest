from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte Simple de Traspasos con Precio Interno'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids) if docids else self.env['stock.picking'].search([])

        # Busca la lista de precios "Interno (CLP)"
        pricelist = self.env['product.pricelist'].search([('name', '=', 'Interno (CLP)')], limit=1)
        precios_interno = {}
        if pricelist:
            for picking in pickings:
                for ml in picking.move_line_ids_without_package:
                    product = ml.product_id
                    if not product or product.id in precios_interno:
                        continue
                    item = self.env['product.pricelist.item'].search([
                        ('pricelist_id', '=', pricelist.id),
                        ('product_tmpl_id', '=', product.product_tmpl_id.id),
                        ('applied_on', '=', '1_product'),
                    ], limit=1)
                    precio = item.fixed_price if item else 0.0
                    precios_interno[product.id] = precio

        return {
            'docs': pickings,
            'precios_interno': precios_interno,   # <- ESTE NOMBRE EXACTO
        }
