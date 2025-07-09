from odoo import models
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class CobroTallerXlsx(ReportXlsx):
    _name = 'report.joyeria_reparaciones.cobro_taller_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Cobro Taller en Excel'

    def generate_xlsx_report(self, workbook, data, records):
        sheet = workbook.add_worksheet("Cobro Taller")
        bold  = workbook.add_format({'bold': True})
        headers = [
            'RMA','Metal Utilizado','Peso','Metales Extra',
            'Cobro Interno','Hechura','Cobros Extras','Total'
        ]
        for col, h in enumerate(headers):
            sheet.write(0, col, h, bold)
        row = 1
        for rec in records:
            sheet.write(row, 0, rec.name)
            sheet.write(row, 1, rec.metal_utilizado or '')
            sheet.write(row, 2, rec.peso_valor or 0.0)
            sheet.write(row, 3, rec.metales_extra  or 0.0)
            sheet.write(row, 4, rec.cobro_interno  or 0.0)
            sheet.write(row, 5, rec.hechura        or 0.0)
            sheet.write(row, 6, rec.cobros_extras  or 0.0)
            sheet.write(row, 7, rec.total_salida_taller or 0.0)
            row += 1
