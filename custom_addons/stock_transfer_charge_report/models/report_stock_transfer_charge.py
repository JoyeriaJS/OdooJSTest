from odoo import models, api
from collections import defaultdict
from datetime import datetime

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de Cargos entre Locales por Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].search([])  # sin filtro para test

        data_by_month = defaultdict(list)

        for picking in pickings:
            if not picking.move_line_ids:
                continue
            for line in picking.move_line_ids:
                if not line.product_id or not line.qty_done:
                    continue
                date = picking.date_done or picking.date or datetime.now()
                month_key = date.strftime('%B %Y')
                data_by_month[month_key].append({
                    'origin': picking.location_id.display_name,
                    'destination': picking.location_dest_id.display_name,
                    'product': line.product_id.display_name,
                    'quantity': line.qty_done,
                    'price_unit': line.product_id.standard_price,
                    'subtotal': line.qty_done * line.product_id.standard_price,
                })

        months = [{'month': k, 'lines': v} for k, v in data_by_month.items()]
        if not months:
            # Log en consola del servidor para detectar que está vacío
            print("❌ [REPORTE TRASPASOS] No se encontraron movimientos con qty_done")

        return {
            'months': months,
        }
