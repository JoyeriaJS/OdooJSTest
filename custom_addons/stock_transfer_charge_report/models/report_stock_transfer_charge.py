# -*- coding: utf-8 -*-
from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge'        # ← nombre corto
    _description = 'Reporte Simple de Traspasos'
    _auto = False                                  # ← evita crear tabla

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids) if docids else self.env['stock.picking'].search([])
        pricelist = self.env['product.pricelist'].search([('name','=','Interno (CLP)')], limit=1)
        docs = []
        for p in pickings:
            lines, total_unit, total_int = [], 0.0, 0.0
            for ml in p.move_line_ids_without_package:
                qty       = ml.qty_done or ml.quantity or 0.0
                up        = ml.product_id.standard_price or 0.0
                int_price = 0.0
                if pricelist:
                    item = self.env['product.pricelist.item'].search([
                        ('pricelist_id','=',pricelist.id),
                        ('product_tmpl_id','=',ml.product_id.product_tmpl_id.id),
                        ('applied_on','=','1_product'),
                    ], limit=1)
                    int_price = item.fixed_price or 0.0
                sub_u = qty * up
                sub_i = qty * int_price
                total_unit += sub_u
                total_int  += sub_i
                lines.append({
                    'producto':     ml.product_id.display_name,
                    'cantidad':     qty,
                    'uom':          ml.product_uom_id.name,
                    'price_unit':   up,
                    'price_int':    int_price,
                    'subtotal_unit':sub_u,
                    'subtotal_int': sub_i,
                })
            docs.append({
                'name':          p.name,
                'location':      p.location_id.display_name,
                'location_dest': p.location_dest_id.display_name,
                'state':         p.state,
                'type':          p.picking_type_code,
                'lines':         lines,
                'total_unit':    total_unit,
                'total_int':     total_int,
            })
        return {'docs': docs}
