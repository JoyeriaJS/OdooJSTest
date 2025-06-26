from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import AccessError

class ReportMonthlyRmaPos(models.AbstractModel):
    _name = 'report.joyeria_reparaciones.report_monthly_rma_pos_template'
    _description = 'Reporte Mensual RMA + POS Consolidado'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not self.env.user.has_group('base.group_system'):
            raise AccessError("Sólo los administradores pueden generar este reporte.")
        # Tomamos el año atrás hasta hoy
        date_end = fields.Date.context_today(self)
        date_start = date_end - relativedelta(months=12)

        groups = {}
        # 1) Sumar 'saldo' de joyeria.reparacion por fecha_firma
        reparas = self.env['joyeria.reparacion'].search([
            ('fecha_firma', '>=', date_start),
            ('fecha_firma', '<=', date_end)
        ])
        for r in reparas:
            mes = r.fecha_firma.strftime('%Y-%m')
            groups.setdefault(mes, {'rma_total': 0.0, 'pos_total': 0.0})
            groups[mes]['rma_total'] += r.saldo

        # 2) Sumar ventas POS (amount_total) por date_order
        orders = self.env['pos.order'].search([
            ('date_order', '>=', date_start),
            ('date_order', '<=', date_end)
        ])
        for o in orders:
            # convertimos a datetime para formateo
            dt = fields.Datetime.from_string(o.date_order)
            mes = dt.strftime('%Y-%m')
            groups.setdefault(mes, {'rma_total': 0.0, 'pos_total': 0.0})
            groups[mes]['pos_total'] += o.amount_total

        # 3) Preparamos lista ordenada
        lines = []
        for mes, vals in sorted(groups.items()):
            year, month = mes.split('-')
            month_name = datetime(int(year), int(month), 1).strftime('%B %Y')
            lines.append({
                'month_name': month_name,
                'rma_total': vals['rma_total'],
                'pos_total': vals['pos_total'],
            })

        return {
            'date_start': date_start,
            'date_end': date_end,
            'lines': lines,
        }
