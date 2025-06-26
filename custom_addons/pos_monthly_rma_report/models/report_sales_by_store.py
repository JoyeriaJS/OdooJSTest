from odoo import models, fields, api

class ReportSalesByStore(models.AbstractModel):
    _name = 'report.pos_monthly_rma_report.report_sales_by_store_template'
    _description = 'Monthly RMA and POS Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Fetch all repairs and POS orders
        reparaciones = self.env['joyeria.reparacion'].search([('fecha_firma', '!=', False)])
        pos_orders = self.env['pos.order'].search([])

        # Group data by month-year
        groups = {}
        for r in reparaciones:
            if not r.fecha_firma:
                continue
            key = r.fecha_firma.strftime('%Y-%m')
            grp = groups.setdefault(key, {'date': r.fecha_firma.strftime('%B %Y'), 'rma_total': 0.0, 'pos_total': 0.0})
            grp['rma_total'] += r.saldo or 0.0

        for o in pos_orders:
            if not o.date_order:
                continue
            dt = fields.Datetime.from_string(o.date_order)
            key = dt.strftime('%Y-%m')
            grp = groups.setdefault(key, {'date': dt.strftime('%B %Y'), 'rma_total': 0.0, 'pos_total': 0.0})
            grp['pos_total'] += o.amount_total or 0.0

        # Sort groups by key
        sorted_keys = sorted(groups.keys())
        result = [groups[k] for k in sorted_keys]
        return {'groups': result}