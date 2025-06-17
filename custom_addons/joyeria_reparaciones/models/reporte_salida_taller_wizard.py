# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.exceptions import AccessError
from collections import OrderedDict

class ReportSalidaTaller(models.AbstractModel):
    _name = 'report.joyeria_reparaciones.reporte_salida_taller_template'
    _description = 'Valores para QWeb Reporte Salida Taller'

    @api.model
    def _get_report_values(self, docids, data=None):
        # --- Validación de permisos ---
        if not self.env.user.has_group('base.group_system'):
            raise AccessError("Sólo los administradores pueden generar este reporte.")
        # --------------------------------

        # buscamos las reparaciones seleccionadas
        docs = self.env['joyeria.reparacion'].browse(docids)
        # agrupamos por (año, mes)
        groups = OrderedDict()
        for rec in docs:
            dt = rec.fecha_recepcion
            if not dt:
                continue
            key = (dt.year, dt.month)
            if key not in groups:
                groups[key] = {
                    'docs': [],
                    'sums': {
                        'cobro_interno':        0.0,
                        'hechura':              0.0,
                        'cobros_extras':        0.0,
                        'total_salida_taller':  0.0,
                    }
                }
            grp = groups[key]
            grp['docs'].append(rec)
            grp['sums']['cobro_interno']       += rec.cobro_interno      or 0.0
            grp['sums']['hechura']             += rec.hechura            or 0.0
            grp['sums']['cobros_extras']       += rec.cobros_extras      or 0.0
            grp['sums']['total_salida_taller'] += rec.total_salida_taller or 0.0

        # Preparamos lista ordenada de grupos
        group_list = []
        for (year, month), val in groups.items():
            group_list.append({
                'year':  year,
                'month': month,
                'docs':  val['docs'],
                'sums':  val['sums'],
            })

        return {
            'doc_ids':   docids,
            'doc_model': 'joyeria.reparacion',
            'groups':    group_list,
        }
