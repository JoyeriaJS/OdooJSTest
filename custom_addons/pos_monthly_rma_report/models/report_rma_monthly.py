from odoo import api, models
from datetime import date, timedelta

class ReportRmaMonthly(models.AbstractModel):
    _name = 'report.pos_monthly_rma_report.rma_monthly_template'
    _description = 'Reporte Mensual RMA + POS'

    @api.model
    def _get_report_values(self, docids, data=None):
        today = date.today()
        first_day = today.replace(day=1)
        last_day = today
        groups = []
        d = first_day
        while d <= last_day:
            next_d = d + timedelta(days=1)
            day_str = d.strftime('%Y-%m-%d')
            rma_records = self.env['joyeria.reparacion'].search([
                ('fecha_recepcion', '>=', d),
                ('fecha_recepcion', '<', next_d),
            ])
            rma_total = sum(rma_records.mapped('subtotal'))
            pos_orders = self.env['pos.order'].search([
                ('date_order', '>=', d),
                ('date_order', '<', next_d),
                ('state', 'in', ('paid', 'done')),
            ])
            pos_total = sum(pos_orders.mapped('amount_total'))
            groups.append({
                'date': day_str,
                'rma_total': rma_total,
                'pos_total': pos_total,
            })
            d = next_d
        return {
            'groups': groups,
            'date_start': first_day.strftime('%Y-%m-%d'),
            'date_end': last_day.strftime('%Y-%m-%d'),
        }
