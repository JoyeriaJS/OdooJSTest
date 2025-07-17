# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids or [])

        # Buscamos la pricelist “Interno (CLP)” (o la que contenga “Interno”)
        pricelist = self.env['product.pricelist'].search(
            [('name', 'ilike', 'Interno', 'Interno CLP', 'Mayorista', 'interno', 'INTERNO', 'Interno(CLP)', 'Interno (CLP)')], limit=1
        )

        interno = {}
        if pricelist:
            items = self.env['product.pricelist.item'].search([
                ('pricelist_id', '=', pricelist.id),
                ('compute_price',  '=', 'fixed'),
                ('applied_on',    'in', ['0_product_variant', '1_product']),
            ])
            for item in items:
                price = item.fixed_price or 0.0
                if item.applied_on == '0_product_variant' and item.product_id:
                    interno[item.product_id.id] = price
                elif item.applied_on == '1_product' and item.product_tmpl_id:
                    for var in item.product_tmpl_id.product_variant_ids:
                        interno[var.id] = price

        return {
            'doc_ids': pickings.ids,
            'doc_model': 'stock.picking',
            'docs': pickings,
            'interno': interno,
        }
