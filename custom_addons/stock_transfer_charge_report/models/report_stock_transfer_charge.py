# -*- coding: utf-8 -*-
from odoo import api, models
from collections import defaultdict

class ReportStockTransferCharge(models.AbstractModel):
    """Reporte de Cargos entre Locales por Traspasos."""
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de Cargos entre Locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) Sólo internal transfers DONE
        picks = self.env['stock.picking'].browse(docids).filtered(
            lambda p: p.picking_type_id.code == 'internal' and p.state == 'done'
        )

        # 2) Agrupar por mes/origen/destino
        grouped = defaultdict(float)
        for pick in picks:
            date = pick.date_done or pick.scheduled_date
            month = date.strftime('%Y-%m') if date else 'Sin fecha'
            origin = pick.location_id.display_name
            destination = pick.location_dest_id.display_name

            # Priorizar move_line_ids si existen con quantity>0
            ml_lines = pick.move_line_ids.filtered(lambda ml: ml.quantity > 0)
            if ml_lines:
                for ml in ml_lines:
                    qty = ml.quantity
                    price = ml.product_id.standard_price or 0.0
                    grouped[(month, origin, destination)] += qty * price
            else:
                # fallback a move_ids
                mv_lines = pick.move_ids.filtered(
                    lambda m: (getattr(m, 'quantity_done', 0) or getattr(m, 'product_uom_qty', 0)) > 0
                )
                for mv in mv_lines:
                    qty = getattr(mv, 'quantity_done', 0) or mv.product_uom_qty
                    # precio, si hay price_unit en move, sino estándar
                    price = getattr(mv, 'price_unit', 0.0) or mv.product_id.standard_price or 0.0
                    grouped[(month, origin, destination)] += qty * price

        # 3) Construir lista ordenada
        months = []
        for (month, origin, destination), total in sorted(grouped.items()):
            months.append({
                'month': month,
                'origin': origin,
                'destination': destination,
                'total': total,
            })

        return {
            'doc_ids':   docids,
            'doc_model': 'stock.picking',
            'docs':      picks,
            'months':    months,
        }