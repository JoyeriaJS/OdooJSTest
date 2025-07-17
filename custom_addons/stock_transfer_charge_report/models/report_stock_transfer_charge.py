# -*- coding: utf-8 -*-
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales (costes)'

    @api.model
    def _get_report_values(self, docids=None, data=None):
        # 1) Cargamos los pickings seleccionados
        pickings = self.env['stock.picking'].browse(docids or [])

        # 2) Calculamos un dict { move_line_id: coste_unitario }
        costos = {}
        for picking in pickings:
            for ml in picking.move_line_ids_without_package:
                # standard_price es el coste real de inventario
                costos[ml.id] = ml.product_id.standard_price or 0.0

        return {
            'doc_model': 'stock.picking',
            'doc_ids':   pickings.ids,
            'docs':      pickings,
            'costos':    costos,
        }
