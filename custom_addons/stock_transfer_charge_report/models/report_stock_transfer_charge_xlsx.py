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
        bold  = workbook.add_format({'bold': True})
        money = workbook.add_format({'num_format': '#,##0.00'})

        # Hoja
        sheet = workbook.add_worksheet("Cargos Locales")

        # Encabezados
        headers = [
            'Picking', 'Producto', 'Cantidad', 'UoM', 'Peso (g)',
            'Precio Interno', 'Costo Interno',
        ]
        for col, title in enumerate(headers):
            sheet.write(0, col, title, bold)

        # 1) Obtener la pricelist “Interno”
        pricelist = self.env['product.pricelist'].search(
            [('name', 'ilike', 'Interno', 'Interno (CLP) (CLP)')], limit=1)

        # 2) Construir mapeo {variant_id: precio_fijo}
        precios_interno = {}
        if pricelist:
            items = self.env['product.pricelist.item'].search([
                ('pricelist_id', '=', pricelist.id),
                ('applied_on',    'in', ['0_product_variant', '1_product']),
            ])
            for item in items:
                price = item.fixed_price or 0.0
                if item.applied_on == '0_product_variant' and item.product_id:
                    precios_interno[item.product_id.id] = price
                elif item.applied_on == '1_product' and item.product_tmpl_id:
                    for var in item.product_tmpl_id.product_variant_ids:
                        precios_interno[var.id] = price

        # 3) Llenar filas
        row = 1
        for pick in pickings:
            for ml in pick.move_line_ids_without_package:
                qty = ml.quantity or 0.0
                # Tomamos el precio interno desde el mapeo
                unit_price = precios_interno.get(ml.product_id.id, 0.0)
                cost       = qty * unit_price

                sheet.write(row, 0, pick.name)
                sheet.write(row, 1, ml.product_id.display_name)
                sheet.write_number(row, 2, qty)
                sheet.write(row, 3, ml.product_uom_id.name)
                sheet.write_number(row, 4, ml.product_id.weight or 0.0)
                sheet.write_number(row, 5, unit_price, money)
                sheet.write_number(row, 6, cost, money)
                row += 1

        # 4) Totales generales
        sheet.write(row, 0, 'Totales:', bold)
        # sumatoria de la columna de costos (índice 6, de fila 2 a fila 'row')
        sheet.write_formula(row, 6, f'=SUM(G2:G{row})', money)

        # 5) Auto-ajustar ancho
        for idx in range(len(headers)):
            sheet.set_column(idx, idx, 18)