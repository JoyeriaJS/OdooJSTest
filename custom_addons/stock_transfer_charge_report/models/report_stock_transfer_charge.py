# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) load the pickings
        pickings = self.env['stock.picking'].browse(docids or [])

        # 2) find the “Interno (CLP)” pricelist
        pricelist = self.env['product.pricelist'].search(
            [('name', 'ilike', 'interno')], limit=1)

        # 3) build a dict { variant_id: fixed_price }
        precios_interno = {}
        if pricelist:
            Rule = self.env['product.pricelist.item']
            internal_rules = Rule.search([
                ('pricelist_id', '=', pricelist.id),
                ('applied_on', 'in', ['0_product_variant','1_product']),
            ])
            for rule in internal_rules:
                price = rule.fixed_price or 0.0
                if rule.applied_on == '0_product_variant' and rule.product_id:
                    # applies to one specific variant
                    precios_interno[rule.product_id.id] = price
                elif rule.applied_on == '1_product' and rule.product_tmpl_id:
                    # applies to all variants of a template
                    for var in rule.product_tmpl_id.product_variant_ids:
                        precios_interno[var.id] = price

        return {
            'doc_model':       'stock.picking',
            'doc_ids':         pickings.ids,
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
