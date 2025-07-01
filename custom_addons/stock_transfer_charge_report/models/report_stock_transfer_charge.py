# -*- coding: utf-8 -*-
from odoo import api, models
from collections import defaultdict

class ReportStockTransferCharge(models.AbstractModel):
    """Reporte de Cargos entre Locales por Traspasos."""
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de Cargos entre Locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Buscamos solo pickings internos DONE
        pickings = self.env['stock.picking'].browse(docids).filtered(
            lambda p: p.picking_type_id.code == 'internal' and p.state == 'done'
        )

        # Agrupamos por (mes, origen, destino)
        grouped = defaultdict(float)
        for pick in pickings:
            # Mes en formato "YYYY-MM"
            date = pick.date_done or pick.scheduled_date
            month = date.strftime('%Y-%m') if date else 'Sin fecha'
            origin = pick.location_id.display_name
            dest   = pick.location_dest_id.display_name
            # Iteramos sobre move_line_ids (qty_done)
            for ml in pick.move_line_ids.filtered(lambda l: l.qty_done > 0):
                price = ml.product_id.standard_price or 0.0
                grouped[(month, origin, dest)] += ml.qty_done * price

        # Construimos lista ordenada para QWeb
        months = []
        for (month, origin, dest), total in sorted(grouped.items()):
            months.append({'month': month,
                           'origin': origin,
                           'destination': dest,
                           'total': total})

        return {
            'doc_ids':   docids,
            'doc_model': 'stock.picking',
            'docs':      pickings,
            'months':    months,
        }