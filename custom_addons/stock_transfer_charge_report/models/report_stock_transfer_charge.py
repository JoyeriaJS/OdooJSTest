# -*- coding: utf-8 -*-
from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte Simple de Traspasos con Precio Interno'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) Obtengo los pickings (documentos)
        pickings = self.env['stock.picking'].browse(docids) if docids else self.env['stock.picking'].search([])

        # 2) Busco tu lista de precios interna
        pricelist = self.env['product.pricelist'].search([('name', '=', 'Interno (CLP)')], limit=1)

        # 3) Creo un diccionario ml.id -> precio interno
        precios_interno = {}
        # Recorro todas las líneas sin paquete de esos pickings
        for ml in pickings.mapped('move_line_ids_without_package'):
            price = 0.0
            if pricelist:
                item = self.env['product.pricelist.item'].search([
                    ('pricelist_id', '=', pricelist.id),
                    ('product_tmpl_id', '=', ml.product_id.product_tmpl_id.id),
                    ('applied_on', '=', '1_product'),
                ], limit=1)
                price = item.fixed_price or 0.0
            precios_interno[ml.id] = price

        # 4) Devuelvo todo lo necesario al QWeb
        return {
            'doc_ids': docids,
            'doc_model': 'stock.picking',
            'docs': pickings,
            'precios_interno': precios_interno,
            
        }
