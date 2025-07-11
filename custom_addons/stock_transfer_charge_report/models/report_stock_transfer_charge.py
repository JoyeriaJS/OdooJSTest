# -*- coding: utf-8 -*-
from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'   # coincide con module.report id
    _description = 'Reporte Simple de Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) recupera los pickings seleccionados (o todos si no pasan docids)
        pickings = self.env['stock.picking'].browse(docids) if docids else self.env['stock.picking'].search([])

        # 2) localiza tu tarifario "Interno (CLP)"
        pricelist = self.env['product.pricelist'].search(
            [('name', '=', 'Interno (CLP)')], limit=1)

        # 3) construye un dict { variant_id: fixed_price } buscando:
        #    a) items aplicados a variante (0_product_variant)
        #    b) items aplicados a plantilla (1_product) y los reparta a sus variantes
        precios_interno = {}
        if pricelist:
            # 3a) variantes
            variant_items = self.env['product.pricelist.item'].search([
                ('pricelist_id', '=', pricelist.id),
                ('applied_on',   '=', '0_product_variant'),
                ('product_id', '!=', False),
            ])
            for it in variant_items:
                precios_interno[it.product_id.id] = it.fixed_price or 0.0
            # 3b) plantillas
            template_items = self.env['product.pricelist.item'].search([
                ('pricelist_id',  '=', pricelist.id),
                ('applied_on',    '=', '1_product'),
                ('product_tmpl_id','!=', False),
            ])
            for it in template_items:
                for var in it.product_tmpl_id.product_variant_ids:
                    # solo asigna si no lo hizo un item de variante
                    precios_interno.setdefault(var.id, it.fixed_price or 0.0)

        return {
            'doc_ids':         pickings.ids,
            'doc_model':       'stock.picking',
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
