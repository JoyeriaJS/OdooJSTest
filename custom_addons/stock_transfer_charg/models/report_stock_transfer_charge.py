from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock.report_stock_transfer_charge'
    _description = 'Reporte de Cargos entre Locales por Traspasos'

@api.model
def _get_report_values(self, docids, data=None):
    # Obtiene las entregas internas completadas
    pickings = self.env['stock.picking'].browse(docids) or self.env['stock.picking'].search([
        ('picking_type_code', '=', 'internal'),
        ('state', '=', 'done')
    ])
    groups = {}
    for p in pickings:
        origin = p.location_id.display_name
        destination = p.location_dest_id.display_name
        key = (origin, destination)
        for move in p.move_lines:
            qty = move.quantity_done or 0.0
            price = move.product_id.standard_price or 0.0
            amount = qty * price
            groups.setdefault(key, {
                'origin': origin,
                'destination': destination,
                'total': 0.0,
            })
            groups[key]['total'] += amount
    return {
        'doc_ids': pickings.ids,
        'docs': pickings,
        'lines': list(groups.values()),
         }