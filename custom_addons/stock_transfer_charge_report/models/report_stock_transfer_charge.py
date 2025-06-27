# -*- coding: utf-8 -*-
from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.transfer_charge_report_template'
    _description = 'Reporte de Cargos entre Locales por Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].search([
            ('picking_type_code', '=', 'internal'),
            ('state', '=', 'done')
        ])
        groups = {}
        for p in pickings:
            origin = p.location_id.display_name
            dest = p.location_dest_id.display_name
            key = (origin, dest)
            for move in p.move_lines:
                qty = move.quantity_done or 0.0
                price = move.product_id.standard_price or 0.0
                amount = qty * price
                groups.setdefault(key, {
                    'origin': origin,
                    'destination': dest,
                    'total': 0.0,
                })
                groups[key]['total'] += amount

        return {
            'lines': list(groups.values()),
        }
