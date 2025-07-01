# -*- coding: utf-8 -*-
import logging
from odoo import api, models
from collections import defaultdict

_logger = logging.getLogger(__name__)

class ReportStockTransferCharge(models.AbstractModel):
    """Reporte de Cargos entre Locales por Traspasos."""
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de Cargos entre Locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) Cargar pickings internos DONE
        picks = self.env['stock.picking'].browse(docids).filtered(
            lambda p: p.picking_type_id.code == 'internal' and p.state == 'done'
        )
        _logger.info("[DEBUG] Picks seleccionados (ids): %s", picks.ids)

        grouped = defaultdict(float)
        for pick in picks:
            date = pick.date_done or pick.scheduled_date
            month = date.strftime('%Y-%m') if date else 'Sin fecha'
            origin = pick.location_id.display_name
            destination = pick.location_dest_id.display_name

            # debug líneas
            ml = pick.move_line_ids
            mv = pick.move_ids
            _logger.info("[DEBUG] picking %s move_line_ids quantities: %s", pick.id, ml.mapped('quantity'))
            _logger.info("[DEBUG] picking %s move_ids quantity_done: %s", pick.id, mv.mapped('quantity_done'))

            # Priorizar move_line_ids si existen
            if any(l.quantity > 0 for l in ml):
                for l in ml.filtered(lambda l: l.quantity > 0):
                    grouped[(month, origin, destination)] += l.quantity * (l.product_id.standard_price or 0.0)
            else:
                # fallback a move_ids
                for m in mv.filtered(lambda m: (m.quantity_done or m.product_uom_qty) > 0):
                    qty = m.quantity_done or m.product_uom_qty
                    price = (getattr(m, 'price_unit', 0.0) or m.product_id.standard_price or 0.0)
                    grouped[(month, origin, destination)] += qty * price

        _logger.info("[DEBUG] grouped keys: %s", list(grouped.keys()))

        months = [{
            'month': m,
            'origin': o,
            'destination': d,
            'total': total,
        } for (m, o, d), total in sorted(grouped.items())]

        _logger.info("[DEBUG] months result: %s", months)

        return {
            'doc_ids': docids,
            'doc_model': 'stock.picking',
            'docs': picks,
            'months': months,
        }