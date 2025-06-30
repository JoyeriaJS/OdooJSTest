# -*- coding: utf-8 -*-
from odoo import api, models
from collections import defaultdict

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de Cargos entre Locales por Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) Tomamos sólo los pickings internos DONE pasados al reporte
        pickings = self.env['stock.picking'].browse(docids).\
            filtered(lambda p: p.picking_type_code == 'internal' and p.state == 'done')

        # 2) Agrupamos por mes, origen y destino
        data_by_month = defaultdict(list)
        for pick in pickings:
            # Mes en formato "YYYY-MM"
            month = pick.date_done.strftime('%Y-%m') if pick.date_done else 'Sin fecha'
            origin = pick.location_id.display_name
            dest   = pick.location_dest_id.display_name

            # Recorremos cada movimiento (no move_line_ids, sino move_ids, para qty_done)
            for move in pick.move_ids.filtered(lambda m: m.state == 'done'):
                qty  = move.quantity_done or 0.0
                price = move.product_id.standard_price or 0.0
                data_by_month[(month, origin, dest)].append({
                    'origin':     origin,
                    'dest':       dest,
                    'product':    move.product_id.display_name,
                    'quantity':   qty,
                    'price_unit': price,
                    'subtotal':   qty * price,
                })

        # 3) Construimos la lista de meses y lineas
        months = []
        for (month, origin, dest), lines in sorted(data_by_month.items()):
            months.append({
                'month': month,
                'origin': origin,
                'dest': dest,
                'lines': lines,
            })

        # 4) Si no hay datos, el template mostrará el mensaje por defecto
        return {
            'doc_ids':   docids,
            'doc_model': 'stock.picking',
            'docs':      pickings,
            'months':    months,
        }
