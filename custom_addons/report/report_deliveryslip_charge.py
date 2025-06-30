# -*- coding: utf-8 -*-
from odoo import api, models
from collections import defaultdict

class ReportDeliverySlipCharge(models.AbstractModel):
    """Extiende el reporte de Guía de Despacho para añadir cargos entre talleres."""
    _inherit = 'report.stock.report_deliveryslip'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) Llamamos al padre para mantener la lógica original
        res = super(ReportDeliverySlipCharge, self)._get_report_values(docids, data)
        # 2) Cargamos los pickings
        pickings = self.env['stock.picking'].browse(docids)
        # 3) Agrupar por (mes, origen, destino)
        grouped = defaultdict(float)
        for pick in pickings.filtered(lambda p: p.picking_type_code == 'internal' and p.state == 'done'):
            month = pick.date_done.strftime('%Y-%m') if pick.date_done else 'N/A'
            origin = pick.location_id.display_name
            dest = pick.location_dest_id.display_name
            for line in pick.move_line_ids:
                price = line.product_id.standard_price or 0.0
                grouped[(month, origin, dest)] += line.qty_done * price
        # 4) Crear lista ordenada para QWeb
        res['charge_lines'] = [
            {'month': m, 'origin': o, 'dest': d, 'amount': amt}
            for (m, o, d), amt in sorted(grouped.items())
        ]
        return res
