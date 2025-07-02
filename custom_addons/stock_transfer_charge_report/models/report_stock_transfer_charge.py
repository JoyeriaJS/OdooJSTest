from odoo import models, api
from collections import defaultdict
from datetime import datetime

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte General de Traspasos Agrupado'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids) if docids else self.env['stock.picking'].search([])

        # Agrupa: {mes: {origen: [lineas]}}
        grouped = defaultdict(lambda: defaultdict(list))
        for p in pickings:
            # Toma fecha efectiva, si no, usa fecha programada
            fecha = p.scheduled_date or p.date_done or p.date or datetime.now()
            mes = fecha.strftime('%B %Y')
            origen = p.location_id.display_name

            for ml in p.move_line_ids_without_package:
                grouped[mes][origen].append({
                    'picking': p.name,
                    'fecha': fecha.strftime('%d/%m/%Y %H:%M:%S'),
                    'destino': p.location_dest_id.display_name,
                    'producto': ml.product_id.display_name,
                    'cantidad': ml.quantity,
                    'uom': ml.product_uom_id.name,
                    'precio_unit': ml.product_id.standard_price,
                    'subtotal': ml.quantity * (ml.product_id.standard_price or 0.0)
                })

        # Para el template: lista de meses, cada uno con locales y líneas + total
        meses = []
        for mes, locales in grouped.items():
            locs = []
            for origen, lines in locales.items():
                total = sum(l['subtotal'] for l in lines)
                locs.append({
                    'origen': origen,
                    'total': total,
                    'lines': lines,
                })
            meses.append({
                'mes': mes,
                'locales': locs,
            })

        return {
            'meses': meses,
        }
