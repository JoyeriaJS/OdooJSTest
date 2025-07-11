# -*- coding: utf-8 -*-
from odoo import api, models

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte Simple de Traspasos con Precio Interno'
    _auto = False

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids or [])

        # 1) busco la tarifa “Interno (CLP)”
        pricelist = self.env['product.pricelist'].search(
            [('name', '=', 'Interno (CLP)')], limit=1)

        docs = []
        for p in pickings:
            total_std = 0.0
            total_int = 0.0
            lines = []
            for ml in p.move_line_ids_without_package:
                qty     = ml.qty_done or ml.quantity or 0.0
                std_u   = ml.product_id.standard_price or 0.0
                # precio interno fijo de la variante, si existe
                int_u   = 0.0
                if pricelist:
                    item = self.env['product.pricelist.item'].search([
                        ('pricelist_id',   '=', pricelist.id),
                        ('product_tmpl_id', '=', ml.product_id.product_tmpl_id.id),
                        ('applied_on',      '=', '1_product'),
                    ], limit=1)
                    int_u = item.fixed_price or 0.0

                sub_std = qty * std_u
                sub_int = qty * int_u

                total_std += sub_std
                total_int += sub_int

                lines.append({
                    'producto':      ml.product_id.display_name,
                    'cantidad':      qty,
                    'uom':           ml.product_uom_id.name,
                    'price_unit':    std_u,
                    'price_int':     int_u,
                    'subtotal_std':  sub_std,
                    'subtotal_int':  sub_int,
                })

            docs.append({
                'name':            p.name,
                'origin':          p.location_id.display_name,
                'destination':     p.location_dest_id.display_name,
                'state':           p.state,
                'picking_type':    p.picking_type_code,
                'lines':           lines,
                'total_std':       total_std,
                'total_int':       total_int,
            })

        return {
            'doc_ids':   pickings.ids,
            'doc_model': 'stock.picking',
            'docs':      docs,
        }
