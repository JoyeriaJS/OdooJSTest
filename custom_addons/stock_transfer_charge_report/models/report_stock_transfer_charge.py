# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids=None, data=None):
        # 1) Cargo los pickings seleccionados
        pickings = self.env['stock.picking'].browse(docids or [])

        # 2) Localizo la moneda CLP
        clp = self.env['res.currency'].search([('name', '=', 'CLP')], limit=1)

        # 3) Busco la pricelist “Interno (CLP)” (nombre que contenga “Interno” + moneda CLP)
        Pricelist = self.env['product.pricelist']
        tarif = Pricelist.search([
            ('name', 'ilike', 'Interno'),
            ('currency_id', '=', clp.id),
        ], limit=1)

        # 4) Construyo { variant_id: precio_interno_fijo }
        precios_interno = {}
        if tarif:
            items = self.env['product.pricelist.item'].search([
                ('pricelist_id', '=', tarif.id),
                ('applied_on',    '=', '1_product'),
            ])
            for item in items:
                price = item.fixed_price or 0.0
                # si apuntan a variante concreta
                if item.product_id:
                    precios_interno[item.product_id.id] = price
                # si apuntan a plantilla, todas sus variantes
                elif item.product_tmpl_id:
                    for var in item.product_tmpl_id.product_variant_ids:
                        precios_interno[var.id] = price

        return {
            'doc_model':       'stock.picking',
            'doc_ids':         pickings.ids,
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
