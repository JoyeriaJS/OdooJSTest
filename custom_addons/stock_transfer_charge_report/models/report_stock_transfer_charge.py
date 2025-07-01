# -*- coding: utf-8 -*-
from odoo import api, models
from collections import defaultdict
import calendar

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.report_stock_transfer_charge'
    _description = 'Cargos entre Locales (Agrupado Mensual)'

    @api.model
    def _get_report_values(self, docids, data=None):
        # docids vendrá de los stock.picking seleccionados en el wizard de impresión
        Picking = self.env['stock.picking']
        # solo internal y done
        pickings = Picking.browse(docids).filtered(
            lambda p: p.picking_type_code == 'internal' and p.state == 'done'
        )
        grouped = defaultdict(float)
        for pick in pickings:
            if pick.date_done:
                year = pick.date_done.year
                month = calendar.month_name[pick.date_done.month]
                label = f"{month} {year}"
            else:
                label = 'Sin Fecha'
            origin = pick.location_id.display_name
            dest = pick.location_dest_id.display_name
            for mv in pick.move_ids.filtered(lambda m: m.state == 'done' and m.product_uom_qty):
                grouped[(label, origin, dest)] += mv.product_uom_qty * (mv.product_id.standard_price or 0.0)

        charge_lines = [
            {'month': mon, 'origin': ori, 'dest': dst, 'amount': amt}
            for (mon, ori, dst), amt in sorted(grouped.items())
        ]

        return {
            'doc_ids': docids,
            'doc_model': 'stock.picking',
            'data': data,
            'docs': pickings,
            'charge_lines': charge_lines,
        }
