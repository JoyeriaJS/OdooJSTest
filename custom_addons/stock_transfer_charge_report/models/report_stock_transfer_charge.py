# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) Cargo los pickings
        pickings = self.env['stock.picking'].browse(docids or [])

        # 2) Busco la pricelist "Interno (CLP)" (ajusta si tu empresa la llamó distinto)
        pricelist = self.env['product.pricelist'].search(
            [('name', 'ilike', 'Interno', "Interno (CLP)")], limit=1
        )

        # 3) Construyo un dict { variante_id: precio_fijo_interno }
        precios_interno = {}
        precio_global = 0.0
        if pricelist:
            items = self.env['product.pricelist.item'].search([
                ('pricelist_id', '=', pricelist.id),
                ('compute_price', '=', 'fixed'),
            ])
            for item in items:
                # global
                if item.applied_on == '3_global':
                    precio_global = item.fixed_price or 0.0
                # por categoría
                elif item.applied_on == '2_product_category' and item.categ_id:
                    for tmpl in item.categ_id.product_tmpl_ids:
                        for var in tmpl.product_variant_ids:
                            precios_interno[var.id] = item.fixed_price or 0.0
                # por producto (plantilla)
                elif item.applied_on == '1_product' and item.product_tmpl_id:
                    for var in item.product_tmpl_id.product_variant_ids:
                        precios_interno[var.id] = item.fixed_price or 0.0
                # por variante
                elif item.applied_on == '0_product_variant' and item.product_id:
                    precios_interno[item.product_id.id] = item.fixed_price or 0.0

        # 4) Devuelvo al QWeb
        return {
            'doc_ids':         pickings.ids,
            'doc_model':       'stock.picking',
            'docs':            pickings,
            'precios_interno': precios_interno,
            'precio_global':   precio_global,
        }
