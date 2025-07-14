# models/report_salida_taller_xlsx.py
from collections import OrderedDict
from odoo import models
from odoo.exceptions import AccessError

class ReportSalidaTallerXlsx(models.AbstractModel):
    _name = 'report.joyeria_reparaciones.reporte_salida_taller_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Reporte Salida Taller en Excel'

    def generate_xlsx_report(self, workbook, data, records):
        if not self.env.user.has_group('base.group_system'):
            raise AccessError("Sólo los administradores pueden generar este reporte.")
        
        sheet = workbook.add_worksheet("Salida Taller")
        bold  = workbook.add_format({'bold': True})
        money = workbook.add_format({'num_format': '#,##0.00'})

        # 1) Agrupar records por (año, mes)
        groups = OrderedDict()
        for rec in records:
            dt = rec.fecha_recepcion
            if not dt:
                continue
            key = (dt.year, dt.month)
            groups.setdefault(key, []).append(rec)

        # 2) Iterar grupos
        row = 0
        headers = [
            "RMA",
            "Fecha Recepción",
            "Metal Utilizado",
            "Peso",
            "Metales Extra",
            "Cobro Interno",
            "Hechura",
            "Cobros Extras",
            "Total Salida Taller",
        ]
        for (year, month), recs in groups.items():
            # 2.1) Título de grupo
            sheet.write(row, 0, f"{month:02d}/{year}", bold)
            row += 1
            # 2.2) Cabeceras
            for col, h in enumerate(headers):
                sheet.write(row, col, h, bold)
            row += 1
            # 2.3) Filas de detalle y acumuladores
            sum_peso           = 0.0
            sum_metales_extra  = 0.0
            sum_cobro_int      = 0.0
            sum_hechura        = 0.0
            sum_cobros_extra   = 0.0
            sum_total_salida   = 0.0

            for rec in recs:
                # extraer valores
                peso        = rec.gramos_utilizado       or 0.0
                me_extra    = rec.metales_extra     or 0.0
                cob_int     = rec.cobro_interno     or 0.0
                hechura     = rec.hechura           or 0.0
                cob_extra   = rec.cobros_extras     or 0.0
                total_sal   = rec.total_salida_taller or 0.0

                # acumular
                sum_peso         += peso
                sum_metales_extra+= me_extra
                sum_cobro_int    += cob_int
                sum_hechura      += hechura
                sum_cobros_extra += cob_extra
                sum_total_salida += total_sal

                # escribir fila
                sheet.write(row, 0, rec.name)
                sheet.write(row, 1, rec.fecha_recepcion.strftime("%Y-%m-%d") if rec.fecha_recepcion else "")
                sheet.write(row, 2, rec.metal_utilizado or "")
                sheet.write_number(row, 3, peso, money)
                sheet.write_number(row, 4, me_extra, money)
                sheet.write_number(row, 5, cob_int, money)
                sheet.write_number(row, 6, hechura, money)
                sheet.write_number(row, 7, cob_extra, money)
                sheet.write_number(row, 8, total_sal, money)
                row += 1

            # 2.4) Fila de totales del mes
            sheet.write(row, 0, "Total del mes:", bold)
            sheet.write_number(row, 3, sum_peso,         money)
            sheet.write_number(row, 4, sum_metales_extra,money)
            sheet.write_number(row, 5, sum_cobro_int,    money)
            sheet.write_number(row, 6, sum_hechura,      money)
            sheet.write_number(row, 7, sum_cobros_extra, money)
            sheet.write_number(row, 8, sum_total_salida, money)
            row += 2  # espacio antes del siguiente mes

        # 3) Auto-ajustar ancho de columnas
        for col in range(len(headers)):
            sheet.set_column(col, col, 18)
