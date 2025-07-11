# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    #  EL _name debe coincidir con el atributo name de tu <report> en el XML:
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids or [])

        # 1) buscamos la pricelist que contenga "Interno"
        pricelist = self.env['product.pricelist'].search(
            [('name', 'ilike', 'Interno')], limit=1
        )

        # 2) armamos el dict { variante_id: precio_interno }
        precios_interno = {}
        if pricelist:
            # items aplicables a variante
            variant_items = self.env['product.pricelist.item'].search([
                ('pricelist_id', '=', pricelist.id),
                ('applied_on',   '=', '0_product_variant'),
                ('product_id', '!=', False),
            ])
            for it in variant_items:
                precios_interno[it.product_id.id] = it.fixed_price or 0.0
            # items aplicables a plantilla
            template_items = self.env['product.pricelist.item'].search([
                ('pricelist_id',    '=', pricelist.id),
                ('applied_on',      '=', '1_product'),
                ('product_tmpl_id', '!=', False),
            ])
            for it in template_items:
                for var in it.product_tmpl_id.product_variant_ids:
                    precios_interno.setdefault(var.id, it.fixed_price or 0.0)

        return {
            'doc_ids':         pickings.ids,
            'doc_model':       'stock.picking',
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
