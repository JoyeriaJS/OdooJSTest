# -*- coding: utf-8 -*-
from odoo import api, models
from collections import OrderedDict

class ReportSalesByStore(models.AbstractModel):
    _name = 'report.joyeria_reparaciones.report_sales_by_store_template'
    _description = 'Ventas por Tienda y Mes'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['joyeria.reparacion'].browse(docids).filtered(lambda r: r.fecha_recepcion)
        groups = OrderedDict()
        # Tarifas fijas por metal
        PRICE_ROSADO   = 140000.0
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
                        'peso_valor':        0.0,
                        'metales_extra':     0.0,
                        'precio_unitario':   0.0,
                        'extra':             0.0,
                        'saldo':             0.0,
                        'cobro_interno':     0.0,
                        'hechura':           0.0,
                        'cobros_extras':     0.0,
                        'rosado_weight':     0.0,
                        'amarillo_weight':   0.0,
                        'blanco_weight':     0.0,
                        'plata_weight':      0.0,
                        'rosado_value':      0.0,
                        'amarillo_value':    0.0,
                        'blanco_value':      0.0,
                        'plata_value':       0.0,
                        'total_metales':     0.0,
                        'total_taller':      0.0,
                    }
                }
            grp = groups[key]

            # cálculo de pesos y valores
            w_val   = rec.peso_valor or 0.0
            w_ext   = rec.metales_extra or 0.0
            weight_total = w_val + w_ext

            rosado_w   = 0.0
            amarillo_w = 0.0
            blanco_w   = 0.0
            plata_w    = 0.0
            rosado_v   = 0.0
            amarillo_v = 0.0

            # según metal_utilizado
            if rec.metal_utilizado == 'oro 18k rosado':
                rosado_w   = weight_total
                rosado_v   = weight_total * PRICE_ROSADO
            elif rec.metal_utilizado == 'oro 18k amarillo':
                amarillo_w = weight_total
                amarillo_v = weight_total * PRICE_AMARILLO
            elif rec.metal_utilizado == 'oro 18k blanco':
                blanco_w   = weight_total
                # sin valor definido -> 0
            elif rec.metal_utilizado == 'plata':
                plata_w    = weight_total

            saldo           = (rec.precio_unitario or 0.0) + (rec.extra or 0.0) - (rec.abono or 0.0)
            total_metales   = rosado_v + amarillo_v
            total_taller    = total_metales + \
                              (rec.cobro_interno or 0.0) + \
                              (rec.hechura or 0.0) + \
                              (rec.cobros_extras or 0.0)

            # agregamos la fila
            grp['docs'].append({
                'rec': rec,
                'peso_valor':       w_val,
                'metales_extra':    w_ext,
                'saldo':            saldo,
                'rosado_weight':    rosado_w,
                'amarillo_weight':  amarillo_w,
                'blanco_weight':    blanco_w,
                'plata_weight':     plata_w,
                'rosado_value':     rosado_v,
                'amarillo_value':   amarillo_v,
                'total_metales':    total_metales,
                'total_taller':     total_taller,
            })

            # acumuladores
            s = grp['sums']
            s['peso_valor']      += w_val
            s['metales_extra']   += w_ext
            s['precio_unitario'] += rec.precio_unitario or 0.0
            s['extra']           += rec.extra           or 0.0
            s['saldo']           += saldo
            s['cobro_interno']   += rec.cobro_interno   or 0.0
            s['hechura']         += rec.hechura         or 0.0
            s['cobros_extras']   += rec.cobros_extras   or 0.0
            s['rosado_weight']   += rosado_w
            s['amarillo_weight'] += amarillo_w
            s['blanco_weight']   += blanco_w
            s['plata_weight']    += plata_w
            s['rosado_value']    += rosado_v
            s['amarillo_value']  += amarillo_v
            s['total_metales']   += total_metales
            s['total_taller']    += total_taller

        return {
            'doc_ids':   docids,
            'doc_model': 'joyeria.reparacion',
            'groups':    list(groups.values()),
        }
