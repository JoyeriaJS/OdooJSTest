# -*- coding: utf-8 -*-
from odoo import api, models
from collections import OrderedDict
from odoo.exceptions import AccessError

class ReportSalesByStore(models.AbstractModel):
    _name = 'report.joyeria_reparaciones.report_sales_by_store_template'
    _description = 'Ventas por Tienda y Mes (por Fecha de Firma)'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Sólo admins
        if not self.env.user.has_group('base.group_system'):
            raise AccessError("Sólo los administradores pueden generar este reporte.")

        # filtramos sólo los que tienen fecha de firma
        recs = self.env['joyeria.reparacion'].browse(docids or []).filtered(lambda r: r.fecha_firma)
        groups = OrderedDict()

        for r in recs:
            store = r.local_tienda or 'Sin Tienda'
            dt = r.fecha_firma
            key = (store, dt.year, dt.month)
            if key not in groups:
                groups[key] = {
                    'store': store,
                    'year':  dt.year,
                    'month': dt.month,
                    'docs':  [],
                    'sums': {
                        'gramos_utilizado': 0.0,
                        'cobro_interno':    0.0,
                        'hechura':          0.0,
                        'cobros_extras':    0.0,
                        'pago_taller':      0.0,
                    }
                }
            grp = groups[key]

            # leemos de tu modelo los valores
            metal = r.metal_utilizado     or ''
            gramos = r.gramos_utilizado   or r.peso_total or 0.0
            ci     = r.cobro_interno      or 0.0
            he     = r.hechura            or 0.0
            ce     = r.cobros_extras      or 0.0
            pago   = ci + he + ce

            # apend rows
            grp['docs'].append({
                'rec':              r,
                'metal_utilizado':  metal,
                'gramos_utilizado': gramos,
                'cobro_interno':    ci,
                'hechura':          he,
                'cobros_extras':    ce,
                'pago_taller':      pago,
            })

            # acumula totales
            s = grp['sums']
            s['gramos_utilizado'] += gramos
            s['cobro_interno']    += ci
            s['hechura']          += he
            s['cobros_extras']    += ce
            s['pago_taller']      += pago

        return {
            'doc_ids':   docids,
            'doc_model': 'joyeria.reparacion',
            'groups':    list(groups.values()),
        }
