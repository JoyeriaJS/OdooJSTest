# -*- coding: utf-8 -*-
from odoo import api, models
from collections import OrderedDict
from odoo.exceptions import AccessError

class ReportSalesByStore(models.AbstractModel):
    _name = 'report.joyeria_reparaciones.report_sales_by_store_template'
    _description = 'Ventas por Tienda y Mes'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not self.env.user.has_group('base.group_system'):
            raise AccessError("Sólo los administradores pueden generar este reporte.")
        docs = self.env['joyeria.reparacion'].browse(docids).filtered(lambda r: r.fecha_recepcion)
        groups = OrderedDict()
        # Precios fijos
        PRICE_ROSADO = 140000.0
        PRICE_AMARILLO = 165000.0

        for rec in docs:
            store = rec.local_tienda or 'Sin Tienda'
            dt = rec.fecha_recepcion
            key = (store, dt.year, dt.month)
            if key not in groups:
                groups[key] = {
                    'store': store,
                    'year': dt.year,
                    'month': dt.month,
                    'docs': [],
                    'sums': {
                        'peso_valor':      0.0,
                        'precio_unitario': 0.0,
                        'extra':           0.0,
                        'saldo':           0.0,
                        'cobro_interno':   0.0,
                        'hechura':         0.0,
                        'cobros_extras':   0.0,
                        'rosado':          0.0,
                        'amarillo':        0.0,
                        'total_metales':   0.0,
                        'total_taller':    0.0,
                    }
                }
            grp = groups[key]

            # Cálculos por registro
            weight    = rec.peso_valor or 0.0
            rosado    = weight * PRICE_ROSADO
            amarillo  = weight * PRICE_AMARILLO
            saldo     = (rec.precio_unitario or 0.0) + (rec.extra or 0.0) - (rec.abono or 0.0)
            total_metales = rosado + amarillo
            total_taller  = total_metales + (rec.cobro_interno or 0.0) + (rec.hechura or 0.0) + (rec.cobros_extras or 0.0)

            # Agregar fila al grupo
            grp['docs'].append({
                'rec': rec,
                'weight': weight,
                'saldo': saldo,
                'rosado': rosado,
                'amarillo': amarillo,
                'total_metales': total_metales,
                'total_taller': total_taller,
            })

            # Acumular totales
            s = grp['sums']
            s['peso_valor']      += weight
            s['precio_unitario'] += rec.precio_unitario or 0.0
            s['extra']           += rec.extra           or 0.0
            s['saldo']           += saldo
            s['cobro_interno']   += rec.cobro_interno   or 0.0
            s['hechura']         += rec.hechura         or 0.0
            s['cobros_extras']   += rec.cobros_extras   or 0.0
            s['rosado']          += rosado
            s['amarillo']        += amarillo
            s['total_metales']   += total_metales
            s['total_taller']    += total_taller

        return {
            'doc_ids':   docids,
            'doc_model': 'joyeria.reparacion',
            'groups':    list(groups.values()),
        }