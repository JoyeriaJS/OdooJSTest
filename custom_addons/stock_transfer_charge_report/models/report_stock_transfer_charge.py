# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids or [])

        # Pricelist “Interno (CLP)”
        pricelist = self.env['product.pricelist'].search(
            [('name', 'ilike', 'Interno')], limit=1
        )

        precios_interno = {}
        if pricelist:
            for picking in pickings:
                for ml in picking.move_line_ids_without_package:
                    # aquí forzamos qty=1.0 para obtener el precio unitario
                    price_unit = pricelist.get_product_price(
                        ml.product_id,
                        1.0,
                        ml.product_uom_id.id,
                        picking.partner_id.id or False,
                    )
                    precios_interno[ml.id] = price_unit
        # Si no hay pricelist, todas quedan en 0.0 por defecto
        return {
            'doc_ids':         pickings.ids,
            'doc_model':       'stock.picking',
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
