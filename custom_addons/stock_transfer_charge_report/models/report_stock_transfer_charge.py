# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids=None, data=None):
        # 1) Cargo los pickings seleccionados
        pickings = self.env['stock.picking'].browse(docids or [])

        # 2) Busco la pricelist “Interno (CLP)” (o cualquier que contenga "Interno")
        Tarifas = self.env['product.pricelist']
        Regla   = self.env['product.pricelist.item']
        tarifa = Tarifas.search([('name', 'ilike', 'Interno')], limit=1)

        # 3) Construyo un dict { variant_id: precio_interno }
        precios_interno = {}
        if tarifa:
            items = Regla.search([
                ('pricelist_id', '=', tarifa.id),
                ('applied_on',    '=', '1_product'),
            ])
            for item in items:
                price = item.fixed_price or 0.0
                # Si está ligado a una variante concreta
                if item.product_id:
                    precios_interno[item.product_id.id] = price
                # Si está ligado a una plantilla, aplico a todas sus variantes
                elif item.product_tmpl_id:
                    for var in item.product_tmpl_id.product_variant_ids:
                        precios_interno[var.id] = price

        return {
            'doc_model':       'stock.picking',
            'doc_ids':         pickings.ids,
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
