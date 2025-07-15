# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) cargamos los pickings seleccionados
        pickings = self.env['stock.picking'].browse(docids or [])

        # 2) buscamos la pricelist “Interno (CLP)” (o la que contenga "Interno")
        pricelist = self.env['product.pricelist'].search(
            [('name', 'ilike', 'Interno')], limit=1
        )

        # 3) construimos dict { variant_id: precio_interno }
        precios_interno = {}
        if pricelist:
            # pricelist.item_ids son todas las reglas asociadas
            for item in pricelist.item_ids.filtered(lambda i: i.applied_on == '1_product'):
                price = item.fixed_price or 0.0
                # aplico esa tarifa a cada variante del template
                for var in item.product_tmpl_id.product_variant_ids:
                    precios_interno[var.id] = price

        return {
            'doc_model':       'stock.picking',
            'doc_ids':         pickings.ids,
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
