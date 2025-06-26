from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar
from odoo.exceptions import AccessError

class ReportMonthlyRmaPos(models.AbstractModel):
    _name = 'report.joyeria_reparaciones.report_monthly_rma_pos_template'
    _description = 'Reporte Mensual RMA + POS Consolidado'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Sólo administradores
        if not self.env.user.has_group('base.group_system'):
            raise AccessError("Sólo los administradores pueden generar este reporte.")
        # Hoy
        today = fields.Date.context_today(self)
        # Primer día del mes hace 11 meses
        start_month = (today.replace(day=1) - relativedelta(months=11))
        # Último día del mes actual
        last_day = calendar.monthrange(today.year, today.month)[1]
        end_month = today.replace(day=last_day)

        # Prepara agrupador
        groups = {}
        # 1) Todos los RMA firmados en ese rango
        reparas = self.env['joyeria.reparacion'].search([
            ('fecha_firma', '>=', start_month),
            ('fecha_firma', '<=', end_month),
        ])
        for r in reparas:
            dt = fields.Datetime.to_datetime(r.fecha_firma)
            mes = dt.strftime('%Y-%m')
            groups.setdefault(mes, {'rma_total': 0.0, 'pos_total': 0.0})
            groups[mes]['rma_total'] += r.saldo

        # 2) Todas las ventas POS en ese rango
        orders = self.env['pos.order'].search([
            ('date_order', '>=', start_month),
            ('date_order', '<=', end_month),
        ])
        for o in orders:
            dt = fields.Datetime.from_string(o.date_order)
            mes = dt.strftime('%Y-%m')
            groups.setdefault(mes, {'rma_total': 0.0, 'pos_total': 0.0})
            groups[mes]['pos_total'] += o.amount_total

        # 3) Lista ordenada de meses
        lines = []
        for mes, vals in sorted(groups.items()):
            year, month = map(int, mes.split('-'))
            month_name = datetime(year, month, 1).strftime('%B %Y')
            lines.append({
                'month_name': month_name,
                'rma_total': vals['rma_total'],
                'pos_total': vals['pos_total'],
            })

        return {
            'date_start': start_month,
            'date_end': end_month,
            'lines': lines,
        }
