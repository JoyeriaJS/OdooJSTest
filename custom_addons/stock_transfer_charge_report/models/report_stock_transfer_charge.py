# -*- coding: utf-8 -*-
from odoo import api, models, _
from odoo.exceptions import UserError

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) obtenemos los pickings
        pickings = self.env['stock.picking'].browse(docids or [])
        # 2) buscamos la pricelist interna (con fallback a “Interno” si no existiera)
        pricelist = self.env['product.pricelist'].search(
            [('name', 'ilike', 'Interno')], limit=1)
        if not pricelist:
            raise UserError(_('No se encontró la lista de precios interna (Interno CLP).'))

        # 3) obtenemos precio interno para cada variante en las líneas
        precios_interno = {}
        for picking in pickings:
            for ml in picking.move_line_ids_without_package:
                # Odoo 17: get_product_price devuelve el precio fijo segun la regla
                price = pricelist.get_product_price(
                    ml.product_id,
                    ml.quantity or 0.0,
                    ml.product_uom_id.id,
                    picking.partner_id.id or False,
                )
                precios_interno[ml.product_id.id] = price

        return {
            'doc_ids':         pickings.ids,
            'doc_model':       'stock.picking',
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
