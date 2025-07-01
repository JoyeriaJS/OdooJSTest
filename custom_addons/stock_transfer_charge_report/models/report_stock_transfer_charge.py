from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte Debug de Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        # ¡No filtra nada, trae todo!
        pickings = self.env['stock.picking'].search([], limit=50)  # Limita a 50 por seguridad

        lines = []
        for picking in pickings:
            lines.append({
                'name': picking.name,
                'state': picking.state,
                'picking_type_code': getattr(picking, 'picking_type_code', 'N/A'),
                'origin': picking.location_id.display_name if picking.location_id else '',
                'destination': picking.location_dest_id.display_name if picking.location_dest_id else '',
                'date': picking.date_done or picking.scheduled_date or picking.date,
            })

        return {'lines': lines}
