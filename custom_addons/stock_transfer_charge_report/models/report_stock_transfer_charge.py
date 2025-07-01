# -*- coding: utf-8 -*-
from odoo import api, models
from collections import defaultdict

class ReportStockTransferCharge(models.AbstractModel):
    """Reporte de Cargos entre Locales por Traspasos usando movimientos."""
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de Cargos entre Locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) Filtrar sólo los pickings internos validados
        pickings = self.env['stock.picking'].browse(docids).filtered(
            lambda p: p.picking_type_id.code == 'internal' and p.state == 'done'
        )

        # 2) Agrupar por (mes, origen, destino)
        grouped = defaultdict(float)
        for pick in pickings:
            date = pick.date_done or pick.scheduled_date
            month = date.strftime('%Y-%m') if date else 'Sin fecha'
            origin = pick.location_id.display_name
            dest   = pick.location_dest_id.display_name
            # Usar move_ids para obtener quantity_done
            for mv in pick.move_ids.filtered(lambda m: m.state == 'done' and m.quantity_done > 0):
                qty   = mv.quantity_done
                # Tomar precio unitario desde estándar o, si existe, price_unit
                price = mv.product_id.standard_price or getattr(mv, 'price_unit', 0.0)
                grouped[(month, origin, dest)] += qty * price

        # 3) Construir lista para plantilla
        months = []
        for (month, origin, dest), total in sorted(grouped.items()):
            months.append({
                'month':       month,
                'origin':      origin,
                'destination': dest,
                'total':       total,
            })

        return {
            'doc_ids':   docids,
            'doc_model': 'stock.picking',
            'docs':      pickings,
            'months':    months,
        }