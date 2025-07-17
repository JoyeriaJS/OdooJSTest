# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) Cargo los pickings seleccionados
        pickings = self.env['stock.picking'].browse(docids or [])

        # 2) Busco la pricelist cuyo nombre **exactamente** sea "Interno"
        tarifa = self.env['product.pricelist'].search(
            [('name', '=', 'Interno')], limit=1)

        # 3) Preparo un dict { move_line_id: precio_interno }
        precios_interno = {}
        if tarifa:
            # Para cada línea de movimiento, pido a la tarifa el precio fijo
            for ml in pickings.mapped('move_line_ids_without_package'):
                qty      = ml.quantity or 0.0
                uom_id   = ml.product_uom_id.id
                partner  = ml.picking_id.partner_id.id or False
                precios_interno[ml.id] = tarifa.get_product_price(
                    ml.product_id, qty, uom_id, partner
                )

        return {
            'doc_model':       'stock.picking',
            'doc_ids':         pickings.ids,
            'docs':            pickings,
            'precios_interno': precios_interno,
        }
