# -*- coding: utf-8 -*-
from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de movimientos con Precio Interno'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) Cargar pickings
        pickings = (self.env['stock.picking'].browse(docids)
                    if docids else
                    self.env['stock.picking'].search([]))

        # 2) Buscar la lista de precios “Interno (CLP)”
        pricelist = self.env['product.pricelist'].search(
            [('name', '=', 'Interno (CLP)')], limit=1)

        # 3) Pre-cargar precios por producto
        precios_map = {}
        if pricelist:
            productos = pickings.mapped('move_line_ids_without_package.product_id')
            for prod in productos:
                item = self.env['product.pricelist.item'].search([
                    ('pricelist_id', '=', pricelist.id),
                    ('applied_on', '=', '1_product'),
                    ('product_tmpl_id', '=', prod.product_tmpl_id.id),
                ], limit=1)
                precios_map[prod.id] = item.fixed_price if item else 0.0

        # 4) Construir lista de movimientos y sumar
        movimientos = []
        total_interno = 0.0
        for picking in pickings:
            for ml in picking.move_line_ids_without_package:
                qty = ml.qty_done or ml.quantity or 0.0
                precio_int = precios_map.get(ml.product_id.id, 0.0)
                subtotal_int = qty * precio_int
                total_interno += subtotal_int

                movimientos.append({
                    'code':              ml.product_id.default_code or '',
                    'name':              ml.product_id.display_name,
                    'qty':               qty,
                    'uom':               ml.product_uom_id.name,
                    'origen':            picking.location_id.display_name,
                    'destino':           picking.location_dest_id.display_name,
                    'picking_name':      picking.name,
                    'fecha':             picking.date_done.strftime('%d/%m/%Y %H:%M:%S') if picking.date_done else '',
                    'estado':            picking.state,
                    'precio_interno':    precio_int,
                    'subtotal_interno':  subtotal_int,
                })
        return {
            'movimientos':    movimientos,
            'total_interno':  total_interno,
        }
