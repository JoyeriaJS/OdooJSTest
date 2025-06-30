from odoo import models, fields, api
from collections import defaultdict
from datetime import datetime

class ReportMonthlyTransferCharges(models.AbstractModel):
    _name = 'report.stock.report_monthly_transfer_charges_template'
    _description = 'Reporte mensual de cargos entre locales por traspasos internos'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].search([
            ('picking_type_code', '=', 'internal'),
            ('state', '=', 'done')
        ])

        lines_by_month = defaultdict(list)

        for picking in pickings:
            fecha = picking.scheduled_date or picking.date_done or picking.create_date
            mes_key = fecha.strftime('%Y-%m')
            for move in picking.move_ids_without_package:
                qty = move.quantity_done
                if qty <= 0:
                    continue
                price = move.product_id.standard_price or 0.0
                total = qty * price

                lines_by_month[mes_key].append({
                    'month': fecha.strftime('%B %Y'),
                    'origin': picking.location_id.display_name,
                    'destination': picking.location_dest_id.display_name,
                    'product': move.product_id.display_name,
                    'total': total
                })

        result_lines = []
        for mes, lines in sorted(lines_by_month.items()):
            for line in lines:
                result_lines.append(line)

        return {
            'lines': result_lines,
        }
