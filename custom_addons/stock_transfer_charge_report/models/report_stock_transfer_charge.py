# report_stock_transfer_charge.py
# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids or [])

        # 1) Recuperamos la pricelist "Interno (CLP)" (o que contenga 'Interno')
        pricelist = self.env['product.pricelist'].search(
            [('name', 'ilike', 'Interno')], limit=1
        )

        # 2) Calculamos el precio interno para cada move_line
        precios_interno = {}
        for picking in pickings:
            partner_id = picking.partner_id.id or False
            for ml in picking.move_line_ids_without_package:
                qty    = ml.quantity or 0.0
                uom_id = ml.product_uom_id.id
                if pricelist:
                    # get_product_price en Odoo 17 devuelve el precio fijo
                    price = pricelist.get_product_price(
                        ml.product_id, qty, uom_id, partner_id
                    )
                else:
                    price = 0.0
                precios_interno[ml.id] = price

        return {
            'doc_ids':         pickings.ids,
            'doc_model':       'stock.picking',
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
