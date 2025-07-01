# -*- coding: utf-8 -*-
from odoo import api, models, fields
from collections import defaultdict

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de Cargos entre Locales por Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Sólo internal y done
        pickings = self.env['stock.picking'].search([
            ('picking_type_code', '=', 'internal'),
            ('state', '=', 'done'),
        ], order='date_done')

        data_by_month = defaultdict(list)
        for pick in pickings:
            date = pick.date_done or pick.scheduled_date or pick.date or fields.Datetime.now()
            month = fields.Datetime.context_timestamp(self, pick, date).strftime('%B %Y')
            for ml in pick.move_line_ids.filtered(lambda l: l.qty_done):
                qty   = ml.qty_done
                pu    = ml.product_id.standard_price or 0.0
                data_by_month[month].append({
                    'origin':      pick.location_id.display_name,
                    'destination': pick.location_dest_id.display_name,
                    'product':     ml.product_id.display_name,
                    'quantity':    qty,
                    'price_unit':  pu,
                    'subtotal':    qty * pu,
                })

        # Convertir a lista ordenada
        months = [
            {'month': m, 'lines': lines}
            for m, lines in data_by_month.items()
        ]
        return {
            'doc_ids':     pickings.ids,
            'doc_model':   'stock.picking',
            'months':      months,
        }
