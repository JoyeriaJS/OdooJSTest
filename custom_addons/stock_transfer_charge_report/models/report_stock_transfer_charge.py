from odoo import api, models, fields
from collections import defaultdict

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].search([
            ('picking_type_code', '=', 'internal'),
            ('state', '=', 'done')
        ])

        data_by_month = defaultdict(list)
        for picking in pickings:
            if not picking.date_done:
                continue
            month_key = fields.Datetime.context_timestamp(picking, picking.date_done).strftime('%B %Y')
            for move in picking.move_line_ids:
                if move.qty_done > 0:
                    data_by_month[month_key].append({
                        'fecha': picking.date_done.strftime('%d-%m-%Y'),
                        'origen': picking.location_id.display_name,
                        'destino': picking.location_dest_id.display_name,
                        'producto': move.product_id.display_name,
                        'cantidad': move.qty_done,
                        'precio': move.product_id.standard_price or 0.0,
                        'subtotal': move.qty_done * (move.product_id.standard_price or 0.0)
                    })

        months = [{'month': m, 'lines': l} for m, l in sorted(data_by_month.items())]

        return {
            'doc_ids': docids,
            'doc_model': 'stock.picking',
            'docs': pickings,
            'months': months,
        }
