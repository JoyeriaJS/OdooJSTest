# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids or [])

        # 1) Pricelist “Interno (CLP)”
        pricelist = self.env['product.pricelist'].search(
            [('name', '=', 'Interno (CLP)')], limit=1)

        # 2) Para cada línea tomamos el precio fijo interno
        precios_interno = {}
        if pricelist:
            for picking in pickings:
                for ml in picking.move_line_ids_without_package:
                    prod = ml.product_id
                    qty  = ml.quantity or 0.0
                    # get_product_price en Odoo17 devuelve el price fijo
                    precio = pricelist.get_product_price(
                        prod, qty, ml.product_uom_id.id, picking.partner_id.id or False
                    )
                    precios_interno[prod.id] = precio
                    

        return {
            'doc_ids':         pickings.ids,
            'doc_model':       'stock.picking',
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
