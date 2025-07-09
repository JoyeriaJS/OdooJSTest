# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import io
import xlsxwriter
from collections import OrderedDict

class ReportSalidaTallerXLSX(http.Controller):

    @http.route('/joyeria_reparaciones/salida_taller_xlsx', type='http', auth='user')
    def salida_taller_xlsx(self, docids=None, **kw):
        # docids vendrá como “1,2,3”
        if isinstance(docids, str):
            docids = [int(x) for x in docids.split(',') if x.isdigit()]
        else:
            docids = request.env.context.get('active_ids', [])
        if not docids:
            return request.not_found()

        Repar = request.env['joyeria.reparacion'].browse(docids)

        # -- Reproducimos la agrupación por año/mes de tu wizard de QWeb --
        groups = OrderedDict()
        for rec in Repar:
            dt = rec.fecha_recepcion
            if not dt:
                continue
            key = (dt.year, dt.month)
            if key not in groups:
                groups[key] = {
                    'docs': [],
                    'sums': {
                        'peso_valor':           0.0,
                        'metales_extra':        0.0,
                        'cobro_interno':        0.0,
                        'hechura':              0.0,
                        'cobros_extras':        0.0,
                        'total_salida_taller':  0.0,
                    }
                }
            grp = groups[key]
            grp['docs'].append(rec)
            grp['sums']['peso_valor']          += rec.peso_valor          or 0.0
            grp['sums']['metales_extra']       += rec.metales_extra       or 0.0
            grp['sums']['cobro_interno']       += rec.cobro_interno       or 0.0
            grp['sums']['hechura']             += rec.hechura             or 0.0
            grp['sums']['cobros_extras']       += rec.cobros_extras       or 0.0
            grp['sums']['total_salida_taller'] += rec.total_salida_taller or 0.0

        # -- Preparamos el XLSX en memoria --
        output = io.BytesIO()
        wb = xlsxwriter.Workbook(output, {'in_memory': True})
        ws = wb.add_worksheet("Salida Taller")

        # Estilos
        bold = wb.add_format({'bold': True})
        # Cabecera de columnas
        headers = [
            'RMA','Metal Utilizado','Peso','Metales Extra',
            'Cobro Interno','Hechura','Cobros Extras','Total Salida Taller'
        ]

        row = 0
        for (year, month), grp in groups.items():
            # Título de grupo
            ws.write(row, 0, f"{month:02d}/{year}", bold)
            row += 1
            # Escribo encabezados
            for col, h in enumerate(headers):
                ws.write(row, col, h, bold)
            row += 1
            # Filas de datos
            for rec in grp['docs']:
                vals = [
                    rec.name,
                    rec.metal_utilizado or '',
                    rec.peso_valor or 0.0,
                    rec.metales_extra or 0.0,
                    rec.cobro_interno or 0.0,
                    rec.hechura or 0.0,
                    rec.cobros_extras or 0.0,
                    rec.total_salida_taller or 0.0,
                ]
                for col, v in enumerate(vals):
                    ws.write(row, col, v)
                row += 1
            # Fila de totales
            sums = grp['sums']
            ws.write(row, 0, "Total del mes:", bold)
            # dejamos Metal Utilizado vacío
            totals_row = [
                '', '',
                sums['peso_valor'],
                sums['metales_extra'],
                sums['cobro_interno'],
                sums['hechura'],
                sums['cobros_extras'],
                sums['total_salida_taller'],
            ]
            for col, v in enumerate(totals_row):
                ws.write(row, col, v, bold)
            row += 2

        wb.close()
        output.seek(0)
        # Devolvemos el XLSX como descarga
        filename = 'reporte_salida_taller.xlsx'
        return request.make_response(
            output.read(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', f'attachment; filename="{filename}"')
            ]
        )
