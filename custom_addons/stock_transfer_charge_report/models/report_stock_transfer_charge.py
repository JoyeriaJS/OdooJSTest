from odoo import models, fields, api
from collections import defaultdict
from datetime import datetime

class ReportMonthlyTransferCharges(models.AbstractModel):
    _name = 'report.stock.report_monthly_transfer_charges_template'
    _description = 'Reporte mensual de cargos entre locales por traspasos internos'

    @api.model
    def _get_report_values(self, docids, data=None):
        moves = self.env['stock.move'].search([
            ('picking_id.picking_type_code', '=', 'internal'),
            ('state', '=', 'done'),
            ('quantity_done', '>', 0),
        ])

        data_by_month = defaultdict(list)

        for move in moves:
            picking = move.picking_id
            if not picking or not picking.date_done:
                continue

            fecha = fields.Datetime.context_timestamp(self, picking.date_done)
            mes = fecha.strftime('%B %Y')

            total = move.quantity_done * (move.product_id.standard_price or 0.0)

            data_by_month[mes].append({
                'origin': move.location_id.display_name or '',
                'destination': move.location_dest_id.display_name or '',
                'product': move.product_id.display_name or '',
                'total': total,
            })

        return {
            'doc_ids': docids,
            'doc_model': 'stock.move',
            'data_by_month': dict(data_by_month),
        }
