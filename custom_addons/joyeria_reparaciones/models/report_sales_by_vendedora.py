# -*- coding: utf-8 -*-
from odoo import api, models
from collections import OrderedDict
from odoo.exceptions import AccessError

class ReportSalesByVendedora(models.AbstractModel):
    _name = 'report.joyeria_reparaciones.report_sales_by_vendedora_template'
    _description = 'Ventas por Vendedora y Mes'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not self.env.user.has_group('base.group_system'):
            raise AccessError("Sólo los administradores pueden generar este reporte.")
        docs = self.env['joyeria.reparacion'].browse(docids)
        groups = OrderedDict()

        for rec in docs:
            vend = rec.firma_id
            dt   = rec.fecha_firma
            if not vend or not dt:
                continue
            key = (vend.id, dt.year, dt.month)
            if key not in groups:
                groups[key] = {
                    'vendedora': vend.name,
                    'year':      dt.year,
                    'month':     dt.month,
                    'docs':      [],
                    'total':     0.0,
                }
            grp = groups[key]
            grp['docs'].append(rec)
            # rec.saldo ya es (precio + extra – abono)
            grp['total'] += rec.saldo or 0.0

        return {
            'doc_ids':   docids,
            'doc_model': 'joyeria.reparacion',
            'groups':    list(groups.values()),
        }
