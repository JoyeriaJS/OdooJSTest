from odoo import models, api
from collections import defaultdict

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte agrupado por mes y local de origen'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids) if docids else self.env['stock.picking'].search([])

        # Agrupar por (mes, origen)
        agrupados = defaultdict(list)
        totales = defaultdict(float)
        for picking in pickings:
            if not picking.date_done:
                continue
            mes = picking.date_done.strftime('%B %Y')  # Ej: "Julio 2025"
            origen = picking.location_id.display_name
            key = (mes, origen)
            for ml in picking.move_line_ids_without_package:
                subtotal = ml.quantity * (ml.product_id.standard_price or 0.0)
                agrupados[key].append({
                    'producto': ml.product_id.display_name,
                    'cantidad': ml.quantity,
                    'uom': ml.product_uom_id.name,
                    'precio_unitario': ml.product_id.standard_price,
                    'subtotal': subtotal,
                    'destino': picking.location_dest_id.display_name,
                    'fecha': picking.date_done.strftime('%d/%m/%Y %H:%M:%S'),
                })
                totales[key] += subtotal

        resumen = []
        for (mes, origen), lines in sorted(agrupados.items()):
            resumen.append({
                'mes': mes,
                'origen': origen,
                'detalles': lines,
                'total': round(totales[(mes, origen)], 2)
            })

        return {
            'doc_ids': pickings.ids,
            'doc_model': 'stock.picking',
            'resumen': resumen,
        }
