# -*- coding: utf-8 -*-
from odoo import api, models, fields
from collections import defaultdict
from datetime import datetime

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de Cargos entre Locales por Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Sólo transfers internos finalizados
        pickings = self.env['stock.picking'].search([
            ('picking_type_code', '=', 'internal'),
            ('state', '=', 'done'),
        ])
        # Agrupamos líneas por mes
        data_by_month = defaultdict(list)
        for picking in pickings:
            # Fecha de cierre
            date = fields.Datetime.from_string(picking.date_done)
            month_key = date.strftime('%B %Y')
            for line in picking.move_line_ids.filtered(lambda l: l.qty_done > 0):
                price_unit = line.product_id.standard_price or 0.0
                qty = line.qty_done
                data_by_month[month_key].append({
                    'origin':      picking.location_id.display_name,
                    'destination': picking.location_dest_id.display_name,
                    'product':     line.product_id.display_name,
                    'quantity':    qty,
                    'price_unit':  price_unit,
                    'subtotal':    qty * price_unit,
                })
        # Ordenamos meses cronológicamente
        def _parse(m):
            return datetime.strptime(m, '%B %Y')
        months = [
            {'month': m, 'lines': lines}
            for m, lines in sorted(data_by_month.items(), key=lambda t: _parse(t[0]))
        ]
        return {
            'doc_ids':   pickings.ids,
            'doc_model': 'stock.picking',
            'months':    months,
        }
