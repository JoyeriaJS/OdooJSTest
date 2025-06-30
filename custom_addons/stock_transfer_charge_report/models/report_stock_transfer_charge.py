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
        ])

        grupos = defaultdict(list)

        for move in moves:
            if move.picking_id.date_done:
                fecha = fields.Datetime.context_timestamp(self, move.picking_id.date_done)
                mes = fecha.strftime('%B %Y')
                origen = move.location_id.display_name
                destino = move.location_dest_id.display_name
                producto = move.product_id.display_name
                costo = move.product_id.standard_price or 0.0
                qty = move.quantity_done or 0.0
                total = costo * qty

                grupos[mes].append({
                    'origin': origen,
                    'destination': destino,
                    'product': producto,
                    'total': total,
                })

        return {
            'data_by_month': grupos,
        }
