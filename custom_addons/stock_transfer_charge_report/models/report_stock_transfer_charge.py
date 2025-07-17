# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) Cargo los pickings
        pickings = self.env['stock.picking'].browse(docids or [])

        # 2) Busco la pricelist “Interno (CLP)” (o cualquier que contenga “Interno”)
        Tarifas = self.env['product.pricelist']
        Regla   = self.env['product.pricelist.item']
        tarifa  = Tarifas.search([('name','ilike','Interno')], limit=1)

        # 3) Recojo todas las reglas de precio internas aplicables a variantes
        precios_interno = {}
        if tarifa:
            items = Regla.search([
                ('pricelist_id', '=', tarifa.id),
                ('applied_on', 'in', ['0_product_variant','1_product']),
            ])
            for item in items:
                price = item.fixed_price or 0.0
                # si la regla es por variante concreta:
                if item.applied_on == '0_product_variant' and item.product_id:
                    precios_interno[item.product_id.id] = price
                # si la regla es por plantilla, la aplico a todas sus variantes:
                elif item.applied_on == '1_product' and item.product_tmpl_id:
                    for var in item.product_tmpl_id.product_variant_ids:
                        precios_interno[var.id] = price

        return {
            'doc_model':       'stock.picking',
            'doc_ids':         pickings.ids,
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
