# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids or [])

        # 1) Buscamos cualquier pricelist cuyo nombre contenga "interno"
        pricelist = (
            self.env['product.pricelist']
            .search([('name', 'ilike', 'interno')], limit=1)
        )

        # 2) Construimos el dict { product_id: precio_interno_fijo }
        precios_interno = {}
        if pricelist:
            prods = pickings.mapped('move_line_ids_without_package.product_id')
            for prod in prods:
                # pedimos 1 unidad sólo para tomar el fixed_price
                precios_interno[prod.id] = pricelist.get_product_price(
                    prod,                     # product.product
                    1.0,                      # qty 1
                    prod.uom_id.id,           # uom
                    False,                    # partner (no importa aquí)
                )

        return {
            'doc_ids':         pickings.ids,
            'doc_model':       'stock.picking',
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
