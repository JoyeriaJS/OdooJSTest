# -*- coding: utf-8 -*-
from odoo import api, models
from collections import defaultdict

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Resumen de Cargos entre Locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) Solo pickings internos validados
        picks = self.env['stock.picking'].browse(docids).filtered(
            lambda p: p.picking_type_id.code == 'internal' and p.state == 'done'
        )

        # 2) Agrupar por mes, origen, destino usando move_ids y product_uom_qty
        grouped = defaultdict(float)
        for pick in picks:
            month = pick.date_done.strftime('%Y-%m') if pick.date_done else 'Sin fecha'
            origin = pick.location_id.display_name
            destination = pick.location_dest_id.display_name
            for move in pick.move_ids.filtered(lambda m: m.state == 'done' and m.product_uom_qty > 0):
                qty   = move.product_uom_qty
                price = move.product_id.standard_price or 0.0
                grouped[(month, origin, destination)] += qty * price

        # 3) Construir lista ordenada para la plantilla
        months = [
            {'month': m, 'origin': o, 'destination': d, 'total': total}
            for (m, o, d), total in sorted(grouped.items())
        ]

        return {
            'doc_ids':   docids,
            'doc_model': 'stock.picking',
            'docs':      picks,
            'months':    months,
        }