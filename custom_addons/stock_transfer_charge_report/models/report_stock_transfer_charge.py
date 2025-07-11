# -*- coding: utf-8 -*-
from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'       # ← ESTE debe coincidir con el XML
    _description = 'Reporte Simple de Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) recupera los pickings
        pickings = self.env['stock.picking'].browse(docids) if docids else self.env['stock.picking'].search([])

        # 2) carga la tarifa "Interno (CLP)" y construye un map { variante_id: precio_interno }
        pricelist = self.env['product.pricelist'].search([('name', '=', 'Interno (CLP)')], limit=1)
        precios_interno = {}
        if pricelist:
            items = self.env['product.pricelist.item'].search([
                ('pricelist_id', '=', pricelist.id),
                ('applied_on',    '=', '1_product'),
            ])
            for item in items:
                for var in item.product_tmpl_id.product_variant_ids:
                    precios_interno[var.id] = item.fixed_price or 0.0

        return {
            'doc_ids':         pickings.ids,
            'doc_model':       'stock.picking',
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
