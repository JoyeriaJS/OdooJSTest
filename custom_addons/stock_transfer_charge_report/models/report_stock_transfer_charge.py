# -*- coding: utf-8 -*-
from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte Simple de Traspasos con Precio Interno'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) recupero los pickings
        pickings = self.env['stock.picking'].browse(docids) if docids else self.env['stock.picking'].search([])

        # 2) obtengo la lista de precios interna
        pricelist = self.env['product.pricelist'].search([('name','=','Interno (CLP)')], limit=1)

        docs = []
        for p in pickings:
            lines = []
            total_unit = 0.0
            total_int  = 0.0
            # 3) recorro cada línea sin paquete
            for ml in p.move_line_ids_without_package:
                qty  = ml.qty_done or ml.quantity or 0.0
                up   = ml.product_id.standard_price or 0.0
                # busco el precio interno para este producto
                int_price = 0.0
                if pricelist:
                    item = self.env['product.pricelist.item'].search([
                        ('pricelist_id','=',pricelist.id),
                        ('product_tmpl_id','=',ml.product_id.product_tmpl_id.id),
                        ('applied_on','=','1_product'),
                    ], limit=1)
                    int_price = item.fixed_price or 0.0
                sub_unit = qty * up
                sub_int  = qty * int_price
                total_unit += sub_unit
                total_int  += sub_int
                lines.append({
                    'producto':      ml.product_id.display_name,
                    'cantidad':      qty,
                    'uom':           ml.product_uom_id.name,
                    'price_unit':    up,
                    'price_int':     int_price,
                    'subtotal_unit': sub_unit,
                    'subtotal_int':  sub_int,
                })
            docs.append({
                'name':            p.name,
                'location':        p.location_id.display_name,
                'location_dest':   p.location_dest_id.display_name,
                'state':           p.state,
                'type':            p.picking_type_code,
                'lines':           lines,
                'total_unit':      total_unit,
                'total_int':       total_int,
            })
        return {
            'docs': docs,
        }
