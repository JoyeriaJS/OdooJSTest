# stock_transfer_charge_monthly/models/report_stock_transfer_charge_monthly.py
from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class ReportStockTransferChargeMonthly(models.AbstractModel):
    _name = 'report.stock_transfer_charge_monthly.stock_transfer_charge_monthly_template'
    _description = 'Reporte Mensual Cargos entre Locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Últimos 12 meses
        date_end = fields.Date.context_today(self)
        date_start = date_end - relativedelta(months=12)
        # Tomar traspasos internos validados en ese periodo
        pickings = self.env['stock.picking'].search([
            ('picking_type_code', '=', 'internal'),
            ('state', '=', 'done'),
            ('date_done', '>=', date_start),
            ('date_done', '<=', date_end),
        ])
        groups = {}
        for p in pickings:
            # Agrupar por mes (YYYY-MM), origen, destino y producto
            mes = p.date_done[:7]
            for move in p.move_lines:
                origin = p.location_id.display_name
                dest = p.location_dest_id.display_name
                product = move.product_id.display_name
                price = move.product_id.standard_price or 0.0
                qty = move.quantity_done or 0.0
                amount = qty * price
                key = (mes, origin, dest, product)
                if key not in groups:
                    groups[key] = {
                        'mes': mes,
                        'origin': origin,
                        'destination': dest,
                        'product': product,
                        'total': 0.0,
                    }
                groups[key]['total'] += amount

        # Formatear líneas y nombre de mes
        lines = []
        for _, vals in sorted(groups.items()):
            year, mon = vals['mes'].split('-')
            vals['month_name'] = datetime(int(year), int(mon), 1).strftime('%B %Y')
            lines.append(vals)

        return {
            'date_start': date_start,
            'date_end': date_end,
            'lines': lines,
        }
