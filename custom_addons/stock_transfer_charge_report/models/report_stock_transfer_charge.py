# -*- coding: utf-8 -*-
from odoo import api, models, fields

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids or [])

        # 1) Buscamos la pricelist Interno (CLP) — o cualquier variante que contenga "Interno"
        pricelist = self.env['product.pricelist'].search(
            [('name', 'ilike', 'Interno')], limit=1
        )

        # 2) Construimos { move_line_id: precio_interno }
        precios_interno = {}
        today = fields.Date.context_today(self)
        for picking in pickings:
            partner = picking.partner_id  # record, no ID
            for ml in picking.move_line_ids_without_package:
                qty = ml.quantity or 0.0
                precio = 0.0
                if pricelist:
                    # Odoo 17: get_product_price(product, quantity, partner, date=False, uom_id=False)
                    precio = pricelist.get_product_price(
                        ml.product_id,
                        qty,
                        partner,
                        date=today,
                        uom_id=ml.product_uom_id.id
                    )
                precios_interno[ml.id] = precio

        return {
            'doc_ids':         pickings.ids,
            'doc_model':       'stock.picking',
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
