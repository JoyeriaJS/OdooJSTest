# -*- coding: utf-8 -*-
from odoo import api, models
from collections import defaultdict
from datetime import datetime

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de Cargos entre Locales por Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Sólo internal transfers hechos
        pickings = self.env['stock.picking'].search([
            ('picking_type_code', '=', 'internal'),
            ('state', '=', 'done'),
        ])

        data_by_month = defaultdict(list)
        for pick in pickings:
            # Fecha para agrupar
            date = pick.date_done or pick.scheduled_date or pick.date or datetime.now()
            month_key = date.strftime('%B %Y')
            # Recorremos cada stock.move concluido
            for mv in pick.move_ids.filtered(lambda m: m.state == 'done' and m.product_uom_qty):
                qty = mv.product_uom_qty
                unit_price = mv.product_id.standard_price or 0.0
                subtotal = qty * unit_price
                data_by_month[month_key].append({
                    'origin': pick.location_id.display_name,
                    'destination': pick.location_dest_id.display_name,
                    'product':   mv.product_id.display_name,
                    'quantity':  qty,
                    'price_unit': unit_price,
                    'subtotal':  subtotal,
                })

        # Construimos la lista que consume el QWeb
        months = [
            {'month': month, 'lines': lines}
            for month, lines in sorted(data_by_month.items())
        ]

        return {
            'doc_ids':    pickings.ids,
            'doc_model':  'stock.picking',
            'data':       data,
            'months':     months,
        }
