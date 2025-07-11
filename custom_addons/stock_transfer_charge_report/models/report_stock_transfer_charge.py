# -*- coding: utf-8 -*-
from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte Simple de Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        # pickings
        pickings = self.env['stock.picking'].browse(docids) \
                   if docids else self.env['stock.picking'].search([])

        # pricelist "Interno (CLP)"
        pricelist = self.env['product.pricelist'].search(
            [('name','=','Interno (CLP)')], limit=1)

        # arma mapa product_id → precio_interno
        precios = {}
        for prod in pickings.mapped('move_line_ids_without_package.product_id'):
            precios[prod.id] = 0.0
            if pricelist:
                item = self.env['product.pricelist.item'].search([
                    ('pricelist_id','=',pricelist.id),
                    ('product_tmpl_id','=',prod.product_tmpl_id.id),
                    ('applied_on','=','1_product'),
                ], limit=1)
                precios[prod.id] = item.fixed_price or 0.0

        return {
            'doc_ids':         docids,
            'doc_model':       'stock.picking',
            'docs':            pickings,
            # metemos el diccionario dentro de data
            'data': {
                'precios_interno': precios
            },
        }
