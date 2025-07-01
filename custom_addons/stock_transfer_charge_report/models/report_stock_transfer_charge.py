# -*- coding: utf-8 -*-
from odoo import api, models

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Resumen de Traspasos Internos'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) Solo pickings tipo internal y estado done
        picks = self.env['stock.picking'].browse(docids).filtered(
            lambda p: p.picking_type_code == 'internal' and p.state == 'done'
        )
        # 2) Preparamos líneas sencillas
        lines = []
        for p in picks:
            lines.append({
                'sequence':    p.name,
                'origin':      p.location_id.display_name,
                'destination': p.location_dest_id.display_name,
            })
        return {
            'doc_ids':   docids,
            'doc_model': 'stock.picking',
            'docs':      picks,
            'lines':     lines,
        }
