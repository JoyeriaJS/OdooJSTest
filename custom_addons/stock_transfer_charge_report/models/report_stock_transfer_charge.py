# -*- coding: utf-8 -*-
from odoo import api, models
from collections import defaultdict
import calendar

class ReportDeliverySlipCharge(models.AbstractModel):
    _inherit = 'report.stock.report_deliveryslip'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Llamamos al padre para mantener todo lo original
        res = super(ReportDeliverySlipCharge, self)._get_report_values(docids, data)
        # Filtramos solo transfers internos completados
        pickings = self.env['stock.picking'].browse(docids).filtered(
            lambda p: p.picking_type_code == 'internal' and p.state == 'done'
        )
        grouped = defaultdict(float)
        for pick in pickings:
            if pick.date_done:
                year = pick.date_done.year
                month_num = pick.date_done.month
                month = f"{calendar.month_name[month_num]} {year}"
            else:
                month = 'Sin Fecha'
            origin = pick.location_id.display_name
            dest = pick.location_dest_id.display_name
            for mv in pick.move_ids.filtered(lambda m: m.state == 'done' and m.product_uom_qty):
                grouped[(month, origin, dest)] += mv.product_uom_qty * (mv.product_id.standard_price or 0.0)
        # Construimos lista ordenada
        res['charge_lines'] = [
            {'month': m, 'origin': o, 'dest': d, 'amount': amt}
            for (m, o, d), amt in sorted(grouped.items())
        ]
        return res
