# -*- coding: utf-8 -*-
from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte Simple de Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) Pickings seleccionados (o todos si no docids)
        pickings = self.env['stock.picking'].browse(docids) if docids else self.env['stock.picking'].search([])

        # 2) Buscamos la pricelist “Interno (CLP)”
        pricelist = self.env['product.pricelist'].search([('name','=','Interno (CLP)')], limit=1)

        # 3) Preparamos un mapa { product_id → precio_interno }
        precios_interno = {}
        productos = pickings.mapped('move_line_ids_without_package.product_id')
        for producto in productos:
            # Precio por defecto 0.0
            precios_interno[producto.id] = 0.0
            if pricelist:
                item = self.env['product.pricelist.item'].search([
                    ('pricelist_id','=',pricelist.id),
                    ('product_tmpl_id','=',producto.product_tmpl_id.id),
                    ('applied_on','=','1_product'),
                ], limit=1)
                precios_interno[producto.id] = item.fixed_price or 0.0

        return {
            'doc_ids':         docids,
            'doc_model':       'stock.picking',
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
