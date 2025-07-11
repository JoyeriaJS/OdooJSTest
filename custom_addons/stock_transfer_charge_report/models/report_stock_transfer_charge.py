# -*- coding: utf-8 -*-
from odoo import api, models

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte Simple de Traspasos'
    _auto = False   # evita que intente crear una tabla

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) los pickings
        pickings = self.env['stock.picking'].browse(docids) \
            if docids else self.env['stock.picking'].search([])

        # 2) la pricelist “Interno (CLP)”
        pricelist = self.env['product.pricelist'].search(
            [('name', '=', 'Interno (CLP)')], limit=1)

        # 3) armo un dict: variant_id -> precio interno
        precios_interno = {}
        # inicializo en 0 para cada variante
        for prod in pickings.mapped('move_line_ids_without_package.product_id'):
            precios_interno[prod.id] = 0.0

        # si existe pricelist, leo sus items (tanto aplicados a plantilla como a variante)
        if pricelist:
            items = self.env['product.pricelist.item'].search([
                ('pricelist_id', '=', pricelist.id),
                ('applied_on', 'in', ['0_product_variant', '1_product']),
                '|',
                  ('product_tmpl_id', 'in', pickings.mapped('move_line_ids_without_package.product_id.product_tmpl_id.id')),
                  ('product_id',        'in', pickings.mapped('move_line_ids_without_package.product_id.id')),
            ])
            for it in items:
                if it.applied_on == '0_product_variant' and it.product_id:
                    precios_interno[it.product_id.id] = it.fixed_price or 0.0
                elif it.applied_on == '1_product' and it.product_tmpl_id:
                    # todos los variantes de ese template
                    for prod in pickings.mapped('move_line_ids_without_package.product_id'):
                        if prod.product_tmpl_id.id == it.product_tmpl_id.id:
                            precios_interno[prod.id] = it.fixed_price or 0.0

        # 4) devolvemos TODO lo que la QWeb espera + nuestro dict
        return {
            'doc_ids':         pickings.ids,
            'doc_model':       'stock.picking',
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
