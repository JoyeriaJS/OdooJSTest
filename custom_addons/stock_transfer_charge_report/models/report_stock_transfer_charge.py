# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids or [])

        # 1) recupero la pricelist "Interno (CLP)"
        pricelist = self.env['product.pricelist'].search(
            [('name', '=', 'Interno (CLP)')], limit=1)

        # 2) preparo un dict { move_line_id: precio_interno }
        precios_interno = {}
        if pricelist:
            for item in self.env['product.pricelist.item'].search([
                    ('pricelist_id', '=', pricelist.id),
                    ('applied_on',    '=', '1_product'),
                ]):
                for v in item.product_tmpl_id.product_variant_ids:
                    precios_interno[v.id] = item.fixed_price or 0.0

        # 3) lo paso al QWeb
        return {
            'doc_ids':         pickings.ids,
            'doc_model':       'stock.picking',
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
