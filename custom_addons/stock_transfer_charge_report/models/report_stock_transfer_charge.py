# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) recupera los pickings
        pickings = self.env['stock.picking'].browse(docids or [])

        # 2) busca la pricelist "Interno (CLP)"
        pricelist = self.env['product.pricelist'].search(
            [('name', '=', 'Interno (CLP)')], limit=1
        )

        # 3) construye { move_line_id → precio_interno }
        precios_interno = {}
        for picking in pickings:
            for ml in picking.move_line_ids_without_package:
                if pricelist:
                    precio = pricelist.get_product_price(
                        ml.product_id,
                        ml.quantity or 0.0,
                        ml.product_uom_id.id,
                        picking.partner_id.id or False,
                    )
                else:
                    precio = 0.0
                precios_interno[ml.id] = precio

        return {
            'doc_ids':         pickings.ids,
            'doc_model':       'stock.picking',
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
