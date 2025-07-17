# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids or [])

        # 1) Pricelist “Interno”
        interna = self.env['product.pricelist'].search(
            [('name', '=', 'Interno')], limit=1)

        precios_interno = {}
        quantities       = {}

        # 2) Recorremos todas las move_line_ids_without_package
        for ml in pickings.mapped('move_line_ids_without_package'):
            # calculamos la cantidad real (qty_done si existe, si no ml.quantity)
            qty = getattr(ml, 'qty_done', None)
            if qty is None:
                qty = ml.quantity or 0.0
            quantities[ml.id] = qty

            # calculamos el precio interno
            if interna:
                price = interna.get_product_price(
                    ml.product_id,
                    qty,
                    ml.product_uom_id.id,
                    ml.picking_id.partner_id.id or False
                )
            else:
                price = 0.0
            precios_interno[ml.id] = price

        return {
            'doc_model':       'stock.picking',
            'doc_ids':         pickings.ids,
            'docs':            pickings,
            'precios_interno': precios_interno,
            'quantities':      quantities,
        }
