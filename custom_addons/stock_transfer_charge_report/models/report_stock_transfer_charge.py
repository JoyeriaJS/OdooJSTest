# -*- coding: utf-8 -*-
from odoo import api, models
from collections import defaultdict

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Cargos entre Locales (Agrupado Mensual)'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Seleccionamos sólo los pickings internos DONE
        pickings = (
            self.env['stock.picking']
            .browse(docids)
            .filtered(lambda p: p.picking_type_id.code == 'internal' and p.state == 'done')
        )
        # Agrupamos montos por (mes, origen, destino)
        grouped = defaultdict(float)
        for p in pickings:
            # Mes en formato YYYY-MM
            month = p.date_done.strftime('%Y-%m') if p.date_done else 'Sin Fecha'
            origin = p.location_id.display_name
            dest = p.location_dest_id.display_name
            for mv in p.move_ids.filtered(lambda m: m.state == 'done' and m.product_uom_qty > 0):
                grouped[(month, origin, dest)] += mv.product_uom_qty * (mv.product_id.standard_price or 0.0)
        # Construimos lista para QWeb
        months = [
            {'month': m, 'origin': o, 'dest': d, 'total': amt}
            for (m, o, d), amt in sorted(grouped.items())
        ]
        return {
            'doc_ids':   docids,
            'doc_model': 'stock.picking',
            'docs':      pickings,
            'months':    months,
        }
