# -*- coding: utf-8 -*-
from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte Simple de Traspasos'
    _auto = False  # evita que Odoo intente crear una tabla en la BD

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) recupera los pickings seleccionados
        pickings = self.env['stock.picking'].browse(docids or [])

        # 2) busca la tarifa "Interno (CLP)" y arma un dict {variant_id: precio_interno}
        pricelist = self.env['product.pricelist'].search(
            [('name', '=', 'Interno (CLP)')], limit=1)
        precios_interno = {}
        if pricelist:
            items = self.env['product.pricelist.item'].search([
                ('pricelist_id', '=', pricelist.id),
                ('applied_on',   '=', '1_product'),
            ])
            for item in items:
                for v in item.product_tmpl_id.product_variant_ids:
                    precios_interno[v.id] = item.fixed_price or 0.0

        return {
            'docs':             pickings,
            'precios_interno':  precios_interno,
        }
