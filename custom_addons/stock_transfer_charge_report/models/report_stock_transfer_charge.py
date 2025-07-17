# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids or [])

        # 1) Tarifas y reglas
        Tarifas = self.env['product.pricelist']
        Regla   = self.env['product.pricelist.item']
        tarifa = Tarifas.search([('name', '=', 'Interno (CLP)')], limit=1)

        # 2) Preparamos tres dicts: por variante, por producto, por categoría
        price_variant = {}
        price_product = {}
        price_categ   = {}
        if tarifa:
            items = Regla.search([('pricelist_id','=', tarifa.id)])
            for item in items:
                price = item.fixed_price or 0.0
                if item.applied_on == '0_product_variant' and item.product_tmpl_id:
                    # todas las variantes de esa plantilla
                    for var in item.product_tmpl_id.product_variant_ids:
                        price_variant[var.id] = price
                elif item.applied_on == '1_product' and item.product_id:
                    price_product[item.product_id.id] = price
                elif item.applied_on == '2_product_category' and item.categ_id:
                    price_categ[item.categ_id.id] = price

        # 3) Función auxiliar para resolver precio interno dado un producto
        def get_internal_price(prod):
            # 3.1) por variante
            if prod.id in price_variant:
                return price_variant[prod.id]
            # 3.2) por producto variante->plantilla
            tmpl = prod.product_tmpl_id
            if tmpl and tmpl.id in price_product:
                return price_product[tmpl.id]
            # 3.3) por categoría (sube en el árbol)
            cat = prod.categ_id
            while cat:
                if cat.id in price_categ:
                    return price_categ[cat.id]
                cat = cat.parent_id
            return 0.0

        # 4) Construimos dict { move_line_id: precio_interno }
        precios_interno = {}
        for picking in pickings:
            for ml in picking.move_line_ids_without_package:
                precios_interno[ml.id] = get_internal_price(ml.product_id)

        return {
            'doc_model':       'stock.picking',
            'doc_ids':         pickings.ids,
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
