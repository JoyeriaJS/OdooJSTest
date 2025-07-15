# report_stock_transfer_charge.py
# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids or [])

        # 1) Cargo la Tarifa “Interno” o “Interno (CLP)”
        Tarifa = self.env['product.pricelist']
        regla  = self.env['product.pricelist.item']
        precios_interno = {}

        tarifa = Tarifa.search([('name','ilike','Interno')], limit=1)
        if tarifa:
            # 2) Cojo todas las reglas de precio fijas
            items = regla.search([
                ('pricelist_id','=', tarifa.id),
                ('applied_on',   '=', '1_product'),
            ])
            for item in items:
                fp = item.fixed_price or 0.0
                # Aplica a todas sus variantes:
                for v in item.product_tmpl_id.product_variant_ids:
                    precios_interno[v.id] = fp

        return {
            'doc_model':       'stock.picking',
            'doc_ids':         pickings.ids,
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
