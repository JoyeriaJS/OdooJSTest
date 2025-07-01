# -*- coding: utf-8 -*-
from odoo import api, models

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Resumen de Traspasos Internos'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Cargamos exactamente los pickings que te llegan en docids
        picks = self.env['stock.picking'].browse(docids)
        lines = []
        for p in picks:
            # Independientemente de si tienen movimientos, devolvemos algo
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
