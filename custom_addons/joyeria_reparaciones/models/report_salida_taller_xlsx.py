# models/report_salida_taller_xlsx.py
from odoo import models

class ReportSalidaTallerXlsx(models.AbstractModel):
    _name = 'joyeria_reparaciones.reporte_salida_taller_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Reporte Salida Taller en Excel'

    def generate_xlsx_report(self, workbook, data, records):
        # 1) crear hoja
        sheet = workbook.add_worksheet("Salida Taller")
        # 2) formatos
        bold = workbook.add_format({'bold': True})
        money = workbook.add_format({'num_format': '#,##0.00'})
        # 3) cabeceras
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
        for col, h in enumerate(headers):
            sheet.write(0, col, h, bold)
        # 4) filas de datos
        row = 1
        for rec in records:
            sheet.write(row, 0, rec.name)
            sheet.write(row, 1, rec.fecha_recepcion.strftime("%Y-%m-%d") if rec.fecha_recepcion else "")
            sheet.write(row, 2, rec.metal_utilizado or "")
            sheet.write_number(row, 3, rec.peso_valor or 0.0, money)
            sheet.write_number(row, 4, rec.metales_extra or 0.0, money)
            sheet.write_number(row, 5, rec.cobro_interno or 0.0, money)
            sheet.write_number(row, 6, rec.hechura or 0.0, money)
            sheet.write_number(row, 7, rec.cobros_extras or 0.0, money)
            sheet.write_number(row, 8, rec.total_salida_taller or 0.0, money)
            row += 1
        # 5) autoajustar columnas
        for i in range(len(headers)):
            sheet.set_column(i, i, 18)
