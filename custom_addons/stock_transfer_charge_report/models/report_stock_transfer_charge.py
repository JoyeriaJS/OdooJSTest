# models/report_stock_transfer_charge.py
# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids or [])

        # 1) Pricelist “Interno (CLP)” o “Interno”
        pricelist = self.env['product.pricelist'].search(
            [('name', 'in', ['Interno (CLP)', 'Interno'])],
            limit=1
        )

        precios_interno = {}
        for picking in pickings:
            partner = picking.partner_id.id or False
            for ml in picking.move_line_ids_without_package:
                # Odoo17: get_product_price(product, qty, uom, partner)
                if pricelist:
                    # PASAMOS qty=1.0 para que devuelva precio unitario
                    precio_unit = pricelist.get_product_price(
                        ml.product_id, 1.0, ml.product_uom_id.id, partner
                    )
                else:
                    precio_unit = 0.0
                precios_interno[ml.id] = precio_unit

        return {
            'doc_ids':         pickings.ids,
            'doc_model':       'stock.picking',
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
