# report_stock_transfer_charge.py
# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids or [])

        # 1) obtenemos la pricelist “Interno (CLP)”
        Tarifas = self.env['product.pricelist']
        Regla   = self.env['product.pricelist.item']
        tarifa = Tarifas.search([('name','ilike','Interno')], limit=1)

        # 2) buscamos en las reglas el fixed_price
        precios_interno = {}
        if tarifa:
            # precargamos todas las reglas aplicables a productos
            reglas = Regla.search([
                ('pricelist_id','=', tarifa.id),
                ('applied_on',   '=', '1_product'),
            ])
            # hacemos un dict { template_id: precio }
            precios_por_template = {
                r.product_tmpl_id.id: (r.fixed_price or 0.0)
                for r in reglas
            }
            # ahora recorremos cada linea de picking
            for p in pickings:
                for ml in p.move_line_ids_without_package:
                    tmpl_id = ml.product_id.product_tmpl_id.id
                    precios_interno[ml.id] = precios_por_template.get(tmpl_id, 0.0)

        return {
            'doc_model':       'stock.picking',
            'doc_ids':         pickings.ids,
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
