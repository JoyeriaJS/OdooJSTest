# report_stock_transfer_charge.py
# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) recupera los pickings seleccionados
        pickings = self.env['stock.picking'].browse(docids or [])

        # 2) busca la pricelist “Interno (CLP)” (o cualquier que contenga "Interno")
        pricelist = self.env['product.pricelist'].search(
            [('name', 'ilike', 'Interno')], limit=1
        )

        # 3) construye un dict { move_line_id: precio_interno }
        precios_interno = {}
        if pricelist:
            for picking in pickings:
                for ml in picking.move_line_ids_without_package:
                    qty        = ml.quantity or 0.0
                    uom_id     = ml.product_uom_id.id
                    partner_id = picking.partner_id.id or False
                    precios_interno[ml.id] = pricelist.get_product_price(
                        ml.product_id, qty, uom_id, partner_id
                    ) or 0.0

        return {
            'doc_model':       'stock.picking',
            'doc_ids':         pickings.ids,
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
