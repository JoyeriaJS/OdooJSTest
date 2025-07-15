# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) recupera los pickings seleccionados
        pickings = self.env['stock.picking'].browse(docids or [])

        # 2) busca la pricelist “Interno (CLP)” (o cualquier tarifa que contenga "Interno")
        Pricelist = self.env['product.pricelist']
        Item      = self.env['product.pricelist.item']
        tarifa    = Pricelist.search([('name', 'ilike', 'Interno')], limit=1)

        # 3) construye un dict { move_line_id: precio_interno }
        precios_interno = {}
        if tarifa:
            reglas = Item.search([
                ('pricelist_id', '=', tarifa.id),
                ('applied_on',    '=', '1_product'),
            ])
            for regla in reglas:
                price = regla.fixed_price or 0.0
                # aplica a cada variante del template
                for variant in regla.product_tmpl_id.product_variant_ids:
                    # vamos a indexar por los move_line.id, no por variant,
                    # así que lo dejamos para lookup en el QWeb mediante ml.id
                    precios_interno[variant.id] = price

        return {
            'doc_model':       'stock.picking',
            'doc_ids':         pickings.ids,
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
