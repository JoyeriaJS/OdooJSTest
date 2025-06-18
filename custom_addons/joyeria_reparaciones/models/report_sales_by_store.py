# -*- coding: utf-8 -*-
from odoo import api, models
from collections import OrderedDict
from odoo.exceptions import AccessError

class ReportSalesByStore(models.AbstractModel):
    _name = 'report.joyeria_reparaciones.report_sales_by_store_template'
    _description = 'Reporte de Ventas por Tienda y Mes'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not self.env.user.has_group('base.group_system'):
            raise AccessError("Sólo los administradores pueden generar este reporte.")
        # recortes seleccionados
        docs = self.env['joyeria.reparacion'].browse(docids)
        groups = OrderedDict()

        for rec in docs:
            dt = rec.fecha_recepcion
            store = rec.local_tienda
            if not dt or not store:
                continue
            key = (store, dt.year, dt.month)
            if key not in groups:
                groups[key] = {
                    'store': store,
                    'year': dt.year,
                    'month': dt.month,
                    'docs': [],
                    'sums': {
                        'precio_unitario': 0.0,
                        'extra': 0.0,
                        'abono': 0.0,
                        'saldo': 0.0,
                    }
                }
            grp = groups[key]
            grp['docs'].append(rec)
            grp['sums']['precio_unitario'] += rec.precio_unitario or 0.0
            grp['sums']['extra']             += rec.extra or 0.0
            grp['sums']['abono']             += rec.abono or 0.0
            # saldo = precio + extra – abono
            grp['sums']['saldo']             += (rec.precio_unitario or 0.0) + (rec.extra or 0.0) - (rec.abono or 0.0)

        # pasar a lista (para iteración ordenada en el template)
        group_list = []
        for (store, year, month), val in groups.items():
            group_list.append({
                'store': store,
                'year': year,
                'month': month,
                'docs': val['docs'],
                'sums': val['sums'],
            })

        return {
            'doc_ids':   docids,
            'doc_model': 'joyeria.reparacion',
            'groups':    group_list,
        }
