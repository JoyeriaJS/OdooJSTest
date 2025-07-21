# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.exceptions import AccessError

class ReportStockTransferChargeXlsx(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Cargos entre locales (Excel)'

    def generate_xlsx_report(self, workbook, data, pickings):
        # Sólo administradores
        if not self.env.user.has_group('base.group_system'):
            raise AccessError("Sólo los administradores pueden generar este reporte.")

        # Formatos
        bold = workbook.add_format({'bold': True})
        money = workbook.add_format({'num_format': '#,##0.00'})

        # Hoja
        sheet = workbook.add_worksheet("Cargos Locales")

        # Encabezados
        headers = [
            'Picking', 'Producto', 'Cantidad', 'UoM', 'Peso (g)',
            'Precio Interno', 'Costo Interno'
        ]
        for col, title in enumerate(headers):
            sheet.write(0, col, title, bold)

        # Obtener pricelist interno
        pricelist = self.env['product.pricelist'].search(
            [('name', 'ilike', 'Interno')], limit=1)

        # Filas de datos
        row = 1
        for pick in pickings:
            for ml in pick.move_line_ids_without_package:
                qty = ml.quantity or 0.0
                unit_price = 0.0
                if pricelist:
                    # get_product_price(variant, qty, uom)
                    unit_price = pricelist.get_product_price(
                        ml.product_id, 1, ml.product_uom_id)
                cost = qty * unit_price

                sheet.write(row, 0, pick.name)
                sheet.write(row, 1, ml.product_id.display_name)
                sheet.write_number(row, 2, qty)
                sheet.write(row, 3, ml.product_uom_id.name)
                sheet.write_number(row, 4, ml.product_id.weight or 0.0)
                sheet.write_number(row, 5, unit_price, money)
                sheet.write_number(row, 6, cost, money)
                row += 1

        # Totales generales
        sheet.write(row, 0, 'Totales:', bold)
        # Suma columna Costo Interno (col 6, filas 2 a row)
        sheet.write_formula(row, 6, f'=SUM(G2:G{row})', money)

        # Ajustar ancho automático
        for idx in range(len(headers)):
            sheet.set_column(idx, idx, 18)