# -*- coding: utf-8 -*-
from odoo import models, api

class ReportStockTransfer(models.AbstractModel):
    _name = 'report.stock.report_stock_transfer_document'
    _description = 'Cargos entre Locales por Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Si viene una lista de picking_ids desde la llamada, úsala; 
        # si no, muéstrelo todo
        pickings = self.env['stock.picking'].browse(docids) \
            or self.env['stock.picking'].search([
                ('picking_type_code', '=', 'internal'),
                ('state', '=', 'done')
            ])
        groups = {}
        for p in pickings:
            origin = p.location_id.display_name
            dest   = p.location_dest_id.display_name
            key = (origin, dest)
            for move in p.move_lines:
                qty   = move.quantity_done or 0.0
                price = move.product_id.standard_price or 0.0
                amount = qty * price
                groups.setdefault(key, {
                    'origin': origin,
                    'destination': dest,
                    'total': 0.0,
                })
                groups[key]['total'] += amount

        return {
            'docs': pickings,
            'lines': list(groups.values()),
        }
