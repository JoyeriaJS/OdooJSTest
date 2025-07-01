# -*- coding: utf-8 -*-
from odoo import models, api
from collections import defaultdict
from datetime import datetime

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de Cargos entre Locales por Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Sólo tomamos las pickings seleccionadas y que sean internas y hechas
        pickings = self.env['stock.picking'].browse(docids).filtered(
            lambda p: p.picking_type_code == 'internal' and p.state == 'done'
        )
        data_by_month = defaultdict(list)
        for picking in pickings:
            # Fecha para agrupar por mes
            date = picking.date_done or picking.scheduled_date or picking.date or datetime.now()
            month_key = date.strftime('%B %Y')
            for move in picking.move_ids.filtered(lambda m: m.state=='done' and m.product_uom_qty):
                qty = move.product_uom_qty
                price = move.product_id.standard_price or 0.0
                subtotal = qty * price
                data_by_month[month_key].append({
                    'origin': picking.location_id.display_name,
                    'destination': picking.location_dest_id.display_name,
                    'product': move.product_id.display_name,
                    'quantity': qty,
                    'price_unit': price,
                    'subtotal': subtotal,
                })
        # Construimos la lista final
        months = [
            {'month': m, 'lines': lines}
            for m, lines in sorted(data_by_month.items())
        ]
        return {
            'doc_ids': docids,
            'doc_model': 'stock.picking',
            'months': months,
        }
