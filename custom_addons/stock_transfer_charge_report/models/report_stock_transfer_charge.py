# -*- coding: utf-8 -*-
from odoo import api, models
from collections import defaultdict

class ReportDeliverySlipCharge(models.AbstractModel):
    _inherit = 'report.stock.report_deliveryslip'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Llamamos al padre para conservar toda la lógica original
        res = super(ReportDeliverySlipCharge, self)._get_report_values(docids, data)
        # Filtramos sólo los pickings internos 'done'
        pickings = (
            self.env['stock.picking']
            .browse(docids)
            .filtered(lambda p: p.picking_type_id.code == 'internal' and p.state == 'done')
        )
        # Agrupamos por mes, origen y destino
        grouped = defaultdict(float)
        for p in pickings:
            month = p.date_done.strftime('%Y-%m') if p.date_done else 'Sin Fecha'
            origin = p.location_id.display_name
            dest = p.location_dest_id.display_name
            for mv in p.move_ids.filtered(lambda m: m.state == 'done' and m.product_uom_qty):
                grouped[(month, origin, dest)] += mv.product_uom_qty * (mv.product_id.standard_price or 0.0)
        # Generamos la lista para QWeb
        res['charge_lines'] = [
            {'month': month, 'origin': o, 'dest': d, 'amount': amt}
            for (month, o, d), amt in sorted(grouped.items())
        ]
        return res
