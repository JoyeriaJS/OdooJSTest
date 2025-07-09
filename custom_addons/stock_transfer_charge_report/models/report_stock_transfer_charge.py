# -*- coding: utf-8 -*-
from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge'      # <- nombre corto
    _description = 'Reporte Movimiento entre Locales'
    _auto = False                               # <- no crear tabla en BD

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) recupero los pickings (traslados internos)
        pickings = (
            self.env['stock.picking'].browse(docids)
            if docids else
            self.env['stock.picking'].search([])
        )
        # 2) busco la pricelist interna
        pricelist = self.env['product.pricelist'].search(
            [('name', '=', 'Interno (CLP)')], limit=1
        )
        docs = []
        for p in pickings:
            lines = []
            total_int = 0.0
            for ml in p.move_line_ids_without_package:
                qty = ml.qty_done or ml.quantity or 0.0
                # precio interno por item:
                int_price = 0.0
                if pricelist:
                    item = self.env['product.pricelist.item'].search([
                        ('pricelist_id', '=', pricelist.id),
                        ('product_tmpl_id', '=', ml.product_id.product_tmpl_id.id),
                        ('applied_on', '=', '1_product'),
                    ], limit=1)
                    int_price = item.fixed_price or 0.0
                sub_int = qty * int_price
                total_int += sub_int
                lines.append({
                    'product_code':   ml.product_id.default_code or '',
                    'product_name':   ml.product_id.display_name,
                    'qty':            qty,
                    'uom':            ml.product_uom_id.name,
                    'int_price':      int_price,
                    'subtotal_int':   sub_int,
                })
            docs.append({
                'name':            p.name,
                'origin':          p.location_id.display_name,
                'destination':     p.location_dest_id.display_name,
                'state':           p.state,
                'picking_type':    p.picking_type_code,
                'lines':           lines,
                'total_int':       total_int,
            })
        return {
            'docs': docs,
        }
