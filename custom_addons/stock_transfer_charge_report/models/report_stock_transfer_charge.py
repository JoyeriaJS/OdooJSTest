# -*- coding: utf-8 -*-
from odoo import api, models

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte Simple de Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) Recuperar los pickings a mostrar
        pickings = self.env['stock.picking'].browse(docids) \
            if docids else self.env['stock.picking'].search([])

        # 2) Cargar la pricelist “Interno (CLP)”
        pricelist = self.env['product.pricelist'].search(
            [('name', '=', 'Interno (CLP)')], limit=1)

        # 3) Construir el diccionario {product_id: precio_interno}
        precios_interno = {}
        for prod in pickings.mapped('move_line_ids_without_package.product_id'):
            precios_interno[prod.id] = 0.0
            if pricelist:
                item = self.env['product.pricelist.item'].search([
                    ('pricelist_id', '=', pricelist.id),
                    ('product_tmpl_id', '=', prod.product_tmpl_id.id),
                    ('applied_on', '=', '1_product'),
                ], limit=1)
                precios_interno[prod.id] = item.fixed_price or 0.0

        # 4) Devolver NO sólo los pickings, sino también el mapa de precios
        return {
            'doc_ids':         pickings.ids,
            'doc_model':       'stock.picking',
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
