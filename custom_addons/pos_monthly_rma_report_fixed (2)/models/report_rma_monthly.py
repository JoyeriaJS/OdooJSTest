from odoo import models, fields
from datetime import date
import calendar

class ReportRmaMonthly(models.AbstractModel):
    _name = 'report.pos_monthly_rma_report_fixed.rma_monthly_template'
    _description = 'Reporte Mensual RMA + POS'

    def _get_report_values(self, docids, data=None):
        today = date.today()
        first_day = today.replace(day=1)
        last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1])
        # POS totals by date
        domain_pos = [
            ('session_id.state', '=', 'closed'),
            ('date_order', '>=', first_day),
            ('date_order', '<=', last_day),
        ]
        orders = self.env['pos.order'].search(domain_pos)
        pos_by_day = {}
        for o in orders:
            d = o.date_order.date().isoformat()
            pos_by_day.setdefault(d, 0.0)
            pos_by_day[d] += o.amount_total
        # RMA totals by date
        domain_rma = [
            ('fecha_recepcion', '>=', first_day),
            ('fecha_recepcion', '<=', last_day),
        ]
        rmas = self.env['joyeria.reparacion'].search(domain_rma)
        rma_by_day = {}
        for r in rmas:
            d = fields.Datetime.to_datetime(r.fecha_recepcion).date().isoformat()
            rma_by_day.setdefault(d, 0.0)
            rma_by_day[d] += r.subtotal
        # combine dates
        all_dates = sorted(set(list(pos_by_day.keys()) + list(rma_by_day.keys())))
        groups = []
        for d in all_dates:
            groups.append({
                'date': d,
                'pos_total': pos_by_day.get(d, 0.0),
                'rma_total': rma_by_day.get(d, 0.0),
            })
        return {
            'doc_ids': all_dates,
            'doc_model': 'pos.monthly.rma',
            'date_start': first_day.isoformat(),
            'date_end': last_day.isoformat(),
            'groups': groups,
        }
