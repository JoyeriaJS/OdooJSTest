from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte Simple de Traspasos con Precio Interno'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) obtenemos los pickings
        pickings = self.env['stock.picking'].browse(docids) if docids else self.env['stock.picking'].search([])

        # 2) cargamos la pricelist "Interno (CLP)"
        pricelist = self.env['product.pricelist'].search([('name', '=', 'Interno (CLP)')], limit=1)

        # 3) prepararemos un dict { move_line_id: precio_interno } y sumaremos el total
        precios_interno = {}
        total_interno = 0.0

        for picking in pickings:
            for ml in picking.move_line_ids_without_package:
                qty = ml.quantity or 0.0
                # buscamos el ítem de pricelist para este template
                if pricelist:
                    item = self.env['product.pricelist.item'].search([
                        ('pricelist_id',    '=', pricelist.id),
                        ('product_tmpl_id',  '=', ml.product_id.product_tmpl_id.id),
                        ('applied_on',       '=', '1_product'),
                    ], limit=1)
                    precio_int = item.fixed_price if item else 0.0
                else:
                    precio_int = 0.0

                precios_interno[ml.id] = precio_int
                total_interno += precio_int * qty

        return {
            'docs':             pickings,
            'precios_interno':  precios_interno,
            'total_interno':    total_interno,
        }
