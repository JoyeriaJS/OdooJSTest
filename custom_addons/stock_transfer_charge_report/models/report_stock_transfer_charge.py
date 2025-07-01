# -*- coding: utf-8 -*-
from odoo import api, models
from collections import defaultdict

class ReportDeliverySlipCharge(models.AbstractModel):
    _inherit = 'report.stock.report_deliveryslip'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Llamamos al padre para conservar la lógica estándar
        res = super()._get_report_values(docids, data)
        # Sólo pickings internos ya completados
        pickings = self.env['stock.picking'].browse(docids).filtered(
            lambda p: p.picking_type_id.code == 'internal' and p.state == 'done'
        )
        # Agrupar montos por (mes, origen, destino)
        grouped = defaultdict(float)
        for pick in pickings:
            month = pick.date_done.strftime('%Y-%m') if pick.date_done else 'Sin Fecha'
            origin = pick.location_id.display_name
            dest   = pick.location_dest_id.display_name
            for mv in pick.move_ids.filtered(lambda m: m.state == 'done' and m.product_uom_qty > 0):
                grouped[(month, origin, dest)] += mv.product_uom_qty * (mv.product_id.standard_price or 0.0)
        # Construir lista con picking_id para luego filtrar en QWeb
        charge_lines = []
        for (m, o, d), amt in sorted(grouped.items()):
            # Encontrar uno de los pickings que coincide para asignar picking_id
            for pick in pickings:
                pm = pick.date_done.strftime('%Y-%m') if pick.date_done else 'Sin Fecha'
                if pm == m and pick.location_id.display_name == o and pick.location_dest_id.display_name == d:
                    charge_lines.append({
                        'picking_id': pick.id,
                        'month': m,
                        'origin': o,
                        'dest': d,
                        'amount': amt,
                    })
                    break
        res['charge_lines'] = charge_lines
        return res
