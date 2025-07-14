# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) Cargo los pickings seleccionados
        pickings = self.env['stock.picking'].browse(docids or [])

        # 2) Busco la pricelist “Interno (CLP)” (o “Interno” si así la tienes)
        pricelist = self.env['product.pricelist'].search(
            [('name', 'in', ['Interno (CLP)', 'Interno'])],
            limit=1
        )

        # 3) Calculo el precio interno por cada move_line e indexo por ml.id
        precios_interno = {}
        for picking in pickings:
            for ml in picking.move_line_ids_without_package:
                qty = ml.quantity or 0.0
                uom_id = ml.product_uom_id.id
                partner_id = picking.partner_id.id or False
                if pricelist:
                    # Odoo 17: get_product_price(product, qty, uom, partner)
                    precio = pricelist.get_product_price(
                        ml.product_id, qty, uom_id, partner_id
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
