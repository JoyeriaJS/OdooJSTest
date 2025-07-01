# -*- coding: utf-8 -*-
from odoo import api, models
from collections import defaultdict

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de Cargos entre Locales por Traspasos'
    _inherit = 'report.stock.report_delivery_document'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Obtener pickings internos 'done'
        pickings = self.env['stock.picking'].browse(docids).filtered(
            lambda p: p.picking_type_id.code == 'internal' and p.state == 'done')

        # Agrupar por mes, origen, destino
        grouped = defaultdict(list)
        for pick in pickings:
            month = (pick.date_done or pick.scheduled_date).strftime('%Y-%m')
            origin = pick.location_id.display_name
            dest = pick.location_dest_id.display_name
            for move in pick.move_ids.filtered(lambda m: m.state == 'done'):
                qty = move.quantity_done or 0.0
                price = move.product_id.standard_price or 0.0
                grouped[(month, origin, dest)].append({
                    'product': move.product_id.display_name,
                    'quantity': qty,
                    'price_unit': price,
                    'subtotal': qty * price,
                })

        months = []
        for (month, origin, dest), lines in sorted(grouped.items()):
            months.append({
                'month': month,
                'origin': origin,
                'destination': dest,
                'lines': lines,
            })

        # context for QWeb
        return {
            'doc_ids': docids,
            'doc_model': 'stock.picking',
            'docs': pickings,
            'months': months,
        }
