# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de Cargos entre Locales por Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Buscamos todos los traspasos internos finalizados
        pickings = self.env['stock.picking'].search([
            ('picking_type_code', '=', 'internal'),
            ('state', '=', 'done'),
        ])
        groups = {}
        for p in pickings:
            # Fecha de validación
            dt = fields.Datetime.from_string(p.date_done).date() if p.date_done else False
            if not dt:
                continue
            mes_key = dt.strftime('%Y-%m')
            month_name = datetime(dt.year, dt.month, 1).strftime('%B %Y')
            origin = p.location_id.display_name
            dest = p.location_dest_id.display_name
            for move in p.move_lines:
                prod = move.product_id.display_name
                qty = move.quantity_done or 0.0
                price = move.product_id.standard_price or 0.0
                amount = qty * price
                # clave única por mes, origen, destino y producto
                key = (mes_key, origin, dest, prod)
                groups.setdefault(key, {
                    'month_name': month_name,
                    'origin': origin,
                    'destination': dest,
                    'product': prod,
                    'total': 0.0,
                })
                groups[key]['total'] += amount

        # Convertimos a lista ordenada por fecha
        lines = sorted(groups.values(), key=lambda x: x['month_name'])
        return {
            'lines': lines,
        }
