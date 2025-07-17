# report_stock_transfer_charge.py
# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids or [])

        # 1) Buscamos la tarifa “Interno (CLP)” (o cualquier que contenga “Interno”)
        pricelist = self.env['product.pricelist'].search([('name','ilike','Interno')], limit=1)
        items = pricelist and self.env['product.pricelist.item'].search([
            ('pricelist_id','=',pricelist.id),
            ('applied_on','in',['0_product_variant','1_product'])
        ]) or self.env['product.pricelist.item'].browse()
        # Construyo dict { variant_id: fixed_price }
        precios_interno = {}
        for item in items:
            price = item.fixed_price or 0.0
            if item.applied_on == '0_product_variant' and item.product_id:
                precios_interno[item.product_id.id] = price
            elif item.applied_on == '1_product' and item.product_tmpl_id:
                for var in item.product_tmpl_id.product_variant_ids:
                    precios_interno[var.id] = price

        # 2) Construyo el array de líneas para QWeb
        docs = []
        for picking in pickings:
            for ml in picking.move_line_ids_without_package:
                qty   = ml.quantity or 0.0
                std_c = ml.product_id.standard_price or 0.0
                int_p = precios_interno.get(ml.product_id.id, 0.0)
                docs.append({
                    'picking':     picking.name,
                    'origin':      picking.location_id.display_name,
                    'dest':        picking.location_dest_id.display_name,
                    'state':       picking.state,
                    'type':        picking.picking_type_code,
                    'producto':    ml.product_id.display_name,
                    'qty':         qty,
                    'uom':         ml.product_uom_id.name,
                    'peso':        ml.product_id.weight or 0.0,
                    'coste':       std_c,
                    'precio_int':  int_p,
                    'subtotal_int':qty * int_p,
                })

        return {
            'doc_model': 'stock.picking',
            'doc_ids':   pickings.ids,
            'docs':      docs,
        }
