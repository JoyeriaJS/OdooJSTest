# -*- coding: utf-8 -*-
from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge'
    _description = 'Reporte Simple de Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) recupera los pickings
        pickings = self.env['stock.picking'].browse(docids) if docids else self.env['stock.picking'].search([])

        # 2) carga la tarifa "Interno (CLP)" y construye map { variante_id: precio_interno }
        pricelist = self.env['product.pricelist'].search([('name', '=', 'Interno (CLP)')], limit=1)
        precios_map = {}
        if pricelist:
            items = self.env['product.pricelist.item'].search([
                ('pricelist_id', '=', pricelist.id),
                ('applied_on',    '=', '1_product'),
            ])
            for item in items:
                for var in item.product_tmpl_id.product_variant_ids:
                    precios_map[var.id] = item.fixed_price or 0.0

        # 3) construir lista de dicts
        docs = []
        for p in pickings:
            lines = []
            total_int = 0.0
            for ml in p.move_line_ids_without_package:
                qty    = ml.quantity or 0.0
                unit   = ml.product_id.standard_price or 0.0
                pint   = precios_map.get(ml.product_id.id, 0.0)
                subt_u = qty * unit
                subt_i = qty * pint
                total_int += subt_i
                lines.append({
                    'producto':      ml.product_id.display_name,
                    'cantidad':      qty,
                    'uom':           ml.product_uom_id.name,
                    'precio_unit':   unit,
                    'precio_int':    pint,
                    'subtotal_unit': subt_u,
                    'subtotal_int':  subt_i,
                })
            docs.append({
                'name':             p.name,
                'location':         p.location_id.display_name,
                'location_dest':    p.location_dest_id.display_name,
                'state':            p.state,
                'type':             p.picking_type_code,
                'lines':            lines,
                'total_int':        total_int,
            })
        return {
            'doc_ids':    pickings.ids,
            'doc_model':  'stock.picking',
            'docs':       docs,
        }
