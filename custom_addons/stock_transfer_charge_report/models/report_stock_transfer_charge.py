# -*- coding: utf-8 -*-
from odoo import api, models
from collections import defaultdict

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report_fixed.stock_transfer_charge_report_template'
    _description = 'Reporte de Cargos entre Locales por Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids).filtered(
            lambda p: p.picking_type_id.code == 'internal' and p.state == 'done'
        )
        grouped = defaultdict(float)
        for pick in pickings:
            date = pick.date_done or pick.scheduled_date
            month = date.strftime('%Y-%m') if date else 'Sin fecha'
            origin = pick.location_id.display_name
            dest = pick.location_dest_id.display_name
            for ml in pick.move_line_ids.filtered(lambda l: l.qty_done > 0):
                price = ml.product_id.standard_price or 0.0
                grouped[(month, origin, dest)] += ml.qty_done * price
        months = [{'month': m, 'origin': o, 'destination': d, 'total': total}
                  for (m, o, d), total in sorted(grouped.items())]
        return {
            'doc_ids': docids,
            'doc_model': 'stock.picking',
            'docs': pickings,
            'months': months,
        }
