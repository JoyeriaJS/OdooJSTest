# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.stock_transfer_charge'
    _description = 'Reporte Cargos entre Locales con Precio Interno'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) recogemos los pickings
        pickings = self.env['stock.picking'].browse(docids or [])

        # 2) buscamos la pricelist “Interno (CLP)”
        pricelist = self.env['product.pricelist'].search(
            [('name', '=', 'Interno (CLP)')], limit=1)

        # 3) construimos un dict { variant_id: fixed_price }
        precios_interno = {}
        if pricelist:
            items = self.env['product.pricelist.item'].search([
                ('pricelist_id', '=', pricelist.id),
                ('applied_on',     '=', '1_product'),
            ])
            for it in items:
                for var in it.product_tmpl_id.product_variant_ids:
                    precios_interno[var.id] = it.fixed_price or 0.0

        return {
            'doc_ids':         pickings.ids,
            'doc_model':       'stock.picking',
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
