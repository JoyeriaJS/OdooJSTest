# -*- coding: utf-8 -*-
from odoo import api, models

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte Simple de Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) Recuperar pickings
        pickings = self.env['stock.picking'].browse(docids) \
            if docids else self.env['stock.picking'].search([])

        # 2) Cargar la pricelist “Interno (CLP)”
        pricelist = self.env['product.pricelist'].search(
            [('name', '=', 'Interno (CLP)')], limit=1)

        # 3) Construir el diccionario product_id → precio interno
        precios_interno = {}
        # Inicializo a 0 para todos los productos que aparezcan
        for prod in pickings.mapped('move_line_ids_without_package.product_id'):
            precios_interno[prod.id] = 0.0
        # Si existe pricelist, leo cada ítem
        if pricelist:
            items = self.env['product.pricelist.item'].search([
                ('pricelist_id', '=', pricelist.id),
                ('applied_on', '=', '1_product'),
                ('product_tmpl_id', 'in',
                    pickings.mapped('move_line_ids_without_package.product_id.product_tmpl_id.id'))
            ])
            for it in items:
                # Precio fijo por template
                for prod in pickings.mapped('move_line_ids_without_package.product_id'):
                    if prod.product_tmpl_id.id == it.product_tmpl_id.id:
                        precios_interno[prod.id] = it.fixed_price or 0.0

        # 4) Devolver TODO lo necesario:
        return {
            'doc_ids':         pickings.ids,
            'doc_model':       'stock.picking',
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
