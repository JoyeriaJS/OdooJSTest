# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids or [])

        # 1) Buscar exactamente la Pricelist “Interno”
        interna = self.env['product.pricelist'].search(
            [('name', '=', 'Interno')], limit=1)

        # 2) Calcular precio interno para cada move_line y guardarlo en dict por ml.id
        precios_interno = {}
        if interna:
            for ml in pickings.mapped('move_line_ids_without_package'):
                # ml.qty_done en Odoo17; si no hay qty_done usamos ml.quantity
                qty = getattr(ml, 'qty_done', ml.quantity) or 0.0
                precio = interna.get_product_price(
                    ml.product_id, 
                    qty, 
                    ml.product_uom_id.id,
                    ml.picking_id.partner_id.id or False
                )
                precios_interno[ml.id] = precio

        return {
            'doc_model':       'stock.picking',
            'doc_ids':         pickings.ids,
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
