# -*- coding: utf-8 -*-
from odoo import api, models
from collections import OrderedDict

class ReportPosJr(models.AbstractModel):
    _name = 'report.pos_reparaciones_report.report_pos_jr_template'
    _description = 'Reporte combinado POS y RMA'

    @api.model
    def _get_report_values(self, docids, data=None):
        repairs = self.env['joyeria.reparacion'].search([('fecha_recepcion', '!=', False)])
        orders = self.env['pos.order'].search([('date_order', '!=', False)])
        groups = OrderedDict()

        for rec in repairs:
            dt = rec.fecha_recepcion
            key = (dt.year, dt.month)
            groups.setdefault(key, {'year': dt.year, 'month': dt.month, 'rma_total': 0.0, 'pos_total': 0.0})
            rma_val = (rec.precio_unitario or 0.0) + (rec.extra or 0.0) - (rec.abono or 0.0)
            groups[key]['rma_total'] += rma_val

        for order in orders:
            dt = order.session_id.start_at or order.date_order
            key = (dt.year, dt.month)
            groups.setdefault(key, {'year': dt.year, 'month': dt.month, 'rma_total': 0.0, 'pos_total': 0.0})
            groups[key]['pos_total'] += order.amount_total

        values = []
        for key in sorted(groups):
            grp = groups[key]
            grp['combined_total'] = grp['rma_total'] + grp['pos_total']
            values.append(grp)
        return {'groups': values}
