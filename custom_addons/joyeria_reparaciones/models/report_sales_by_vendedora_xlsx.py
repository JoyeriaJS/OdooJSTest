# -*- coding: utf-8 -*-
from odoo import api, models
from collections import OrderedDict
from odoo.exceptions import AccessError

class ReportSalesByVendedoraXlsx(models.AbstractModel):
    _name = 'joyeria_reparaciones.report_sales_by_vendedora_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Ventas por Vendedora y Mes (Excel)'

    def generate_xlsx_report(self, workbook, data, records):
        # permisos
        if not self.env.user.has_group('base.group_system'):
            raise AccessError("Sólo los administradores pueden generar este reporte.")

        sheet = workbook.add_worksheet("Ventas por Vendedora")
        bold  = workbook.add_format({'bold': True})
        money = workbook.add_format({'num_format': '#,##0.00'})

        # 1) Agrupamos los records por (vendedora, año, mes)
        groups = OrderedDict()
        for rec in records:
            vend = rec.firma_id
            dt   = rec.fecha_firma
            if not vend or not dt:
                continue
            key = (vend.name, dt.year, dt.month)
            groups.setdefault(key, []).append(rec)

        row = 0
        # 2) Iteramos cada grupo
        for (vendedora, year, month), recs in groups.items():
            # 2.1 Título de grupo
            sheet.write(row, 0, f"{vendedora} — {month:02d}/{year}", bold)
            row += 1
            # 2.2 Cabecera de columnas
            headers = ["RMA", "Fecha Firma", "Saldo", "Costo"]
            for col, h in enumerate(headers):
                sheet.write(row, col, h, bold)
            row += 1

            sum_saldo = 0.0
            sum_costo = 0.0
            # 2.3 Filas detalle
            for rec in recs:
                saldo = rec.saldo or 0.0
                costo = rec.subtotal or 0.0
                sum_saldo += saldo
                sum_costo += costo

                sheet.write(row, 0, rec.name)
                sheet.write(row, 1, rec.fecha_firma.strftime("%Y-%m-%d %H:%M:%S"))
                sheet.write_number(row, 2, saldo, money)
                sheet.write_number(row, 3, costo, money)
                row += 1

            # 2.4 Fila totales
            sheet.write(row, 0, "Total del mes:", bold)
            sheet.write_number(row, 2, sum_saldo, money)
            sheet.write_number(row, 3, sum_costo, money)
            row += 2  # espacio antes del siguiente grupo

        # 3) Autoajustar anchos
        sheet.set_column(0, 0, 18)  # RMA
        sheet.set_column(1, 1, 22)  # Fecha Firma
        sheet.set_column(2, 3, 12)  # Saldo, Costo
