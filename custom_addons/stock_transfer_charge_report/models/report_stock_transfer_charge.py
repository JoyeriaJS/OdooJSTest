from odoo import models, api
from collections import defaultdict

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte General de Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids) if docids else self.env['stock.picking'].search([])

        # Agrupar por mes y por destino (local que recibe)
        resumen = defaultdict(lambda: defaultdict(float))
        for picking in pickings:
            fecha = picking.date_done
            if not fecha:
                continue
            mes = fecha.strftime('%B %Y')  # Ejemplo: "July 2025"
            destino = picking.location_dest_id.display_name
            for ml in picking.move_line_ids_without_package:
                subtotal = ml.quantity * (ml.product_id.standard_price or 0.0)
                resumen[mes][destino] += subtotal

        resumen_listo = []
        for mes, destinos in sorted(resumen.items()):
            for destino, total in destinos.items():
                resumen_listo.append({
                    'mes': mes,
                    'destino': destino,
                    'total': round(total, 2),
                })

        return {
            'doc_ids': pickings.ids,
            'doc_model': 'stock.picking',
            'docs': pickings,
            'resumen_mensual': resumen_listo,
        }
