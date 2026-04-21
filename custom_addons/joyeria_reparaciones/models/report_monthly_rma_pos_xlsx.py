# models/report_monthly_rma_pos_xlsx.py
# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.exceptions import AccessError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar

class ReportMonthlyRmaPosXlsx(models.AbstractModel):
    _name = 'report.joyeria_reparaciones.report_monthly_rma_pos_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Reporte Mensual RMA + POS Consolidado (Excel)'

    def generate_xlsx_report(self, workbook, data, records):
        # Sólo administradores
        if not self.env.user.has_group('base.group_system'):
            raise AccessError("Sólo los administradores pueden generar este reporte.")

        # Reutilizamos la lógica del reporte QWeb
        report_qweb  = self.env['report.joyeria_reparaciones.report_monthly_rma_pos_template']
        vals         = report_qweb._get_report_values([], data)
        date_start   = vals['date_start']
        date_end     = vals['date_end']
        lines        = vals['lines']

        # Formatos: negrita y moneda sin decimales con signo $
        bold     = workbook.add_format({'bold': True})
        currency = workbook.add_format({'num_format': '"$"#,##0'})

        sheet = workbook.add_worksheet("RMA+POS Consolidado")
        # Título y rango
        sheet.write(0, 0, "Reporte Mensual RMA + POS Consolidado", bold)
        sheet.write(1, 0, f"Desde: {date_start}    Hasta: {date_end}", bold)

        # Cabeceras
        row = 3
        headers = ["Mes", "Total RMA", "Total POS", "Total Consolidado"]
        for col, h in enumerate(headers):
            sheet.write(row, col, h, bold)
        row += 1

        # Filas
        for line in lines:
            sheet.write(row, 0, line['month_name'])
            # Escribimos enteros con $ y sin decimales
            sheet.write_number(row, 1, int(line['rma_total']), currency)
            sheet.write_number(row, 2, int(line['pos_total']), currency)
            total = line['rma_total'] + line['pos_total']
            sheet.write_number(row, 3, int(total), currency)
            row += 1

        # Auto-ajustar ancho
        for col in range(len(headers)):
            sheet.set_column(col, col, 20)
