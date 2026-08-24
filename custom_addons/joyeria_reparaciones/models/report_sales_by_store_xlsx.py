
# -*- coding: utf-8 -*-
from odoo import models
from collections import OrderedDict
from odoo.exceptions import AccessError


class ReportSalesByStoreXlsx(models.AbstractModel):
    _name = 'report.joyeria_reparaciones.report_sales_by_store_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Ventas por Tienda y Mes (Excel)'

    def generate_xlsx_report(self, workbook, data, records):

        # Sólo admins
        if not self.env.user.has_group('base.group_system'):
            raise AccessError(
                "Sólo los administradores pueden generar este reporte."
            )

        recs = records.filtered(lambda r: r.fecha_firma)

        # =====================================
        # AGRUPAR POR TIENDA
        # =====================================
        stores = OrderedDict()

        for r in recs:
            store = r.local_tienda or 'Sin Tienda'
            stores.setdefault(store, []).append(r)

        # =====================================
        # FORMATOS
        # =====================================
        bold = workbook.add_format({'bold': True})

        title_format = workbook.add_format({
            'bold': True,
            'font_size': 14
        })

        money = workbook.add_format({
            'num_format': '#,##0'
        })

        weight = workbook.add_format({
            'num_format': '#,##0.00'
        })

        datef = workbook.add_format({
            'num_format': 'dd/mm/yyyy'
        })

        total_format = workbook.add_format({
            'bold': True,
            'bg_color': '#D9EAD3',
            'num_format': '#,##0'
        })

        total_weight = workbook.add_format({
            'bold': True,
            'bg_color': '#D9EAD3',
            'num_format': '#,##0.00'
        })

        headers = [
            "RMA",
            "Fecha Firma",
            "Metal Utilizado",
            "Gramos Utilizado",
            "Cobro Interno",
            "Hechura",
            "Cobros Extras",
            "Pago a Taller"
        ]

        # =====================================
        # UNA HOJA POR LOCAL
        # =====================================
        for store, store_recs in stores.items():

            sheet_name = str(store)[:31]
            sheet = workbook.add_worksheet(sheet_name)

            row = 0

            sheet.write(
                row,
                0,
                f"Reporte de Ventas - {store}",
                title_format
            )

            row += 2

            # =====================================
            # RESUMEN DEL LOCAL
            # =====================================

            total_gramos_local = 0

            # Nuevos totales de metales específicos
            total_gramos_oro_amarillo_18k = 0
            total_gramos_oro_rosado_18k = 0

            total_ci_local = 0
            total_he_local = 0
            total_ce_local = 0
            total_pago_local = 0

            for r in store_recs:

                gramos = getattr(
                    r,
                    'gramos_utilizado',
                    None
                ) or getattr(
                    r,
                    'peso_total',
                    0
                )

                ci = r.cobro_interno or 0
                he = r.hechura or 0
                ce = r.cobros_extras or 0

                pago = ci + he + ce

                # =====================================
                # TOTAL GENERAL DE GRAMOS
                # =====================================
                total_gramos_local += gramos

                # =====================================
                # TOTAL GRAMOS POR TIPO DE ORO
                # =====================================
                metal = (r.metal_utilizado or '').strip().lower()

                if 'oro' in metal and '18k' in metal and 'amarillo' in metal:
                    total_gramos_oro_amarillo_18k += gramos

                elif 'oro' in metal and '18k' in metal and 'rosado' in metal:
                    total_gramos_oro_rosado_18k += gramos

                # =====================================
                # TOTALES DE COBROS
                # =====================================
                total_ci_local += ci
                total_he_local += he
                total_ce_local += ce
                total_pago_local += pago

            # =====================================
            # MOSTRAR RESUMEN
            # =====================================

            sheet.write(
                row,
                0,
                "RESUMEN DEL LOCAL",
                bold
            )

            row += 1

            sheet.write(
                row,
                0,
                "Cantidad Trabajos"
            )

            sheet.write(
                row,
                1,
                len(store_recs)
            )

            row += 1

            # -------------------------------------
            # TOTAL GRAMOS
            # -------------------------------------

            sheet.write(
                row,
                0,
                "Total Gramos"
            )

            sheet.write_number(
                row,
                1,
                total_gramos_local,
                weight
            )

            row += 1

            # -------------------------------------
            # ORO AMARILLO 18K
            # -------------------------------------

            sheet.write(
                row,
                0,
                "Total Oro Amarillo 18K"
            )

            sheet.write_number(
                row,
                1,
                total_gramos_oro_amarillo_18k,
                weight
            )

            row += 1

            # -------------------------------------
            # ORO ROSADO 18K
            # -------------------------------------

            sheet.write(
                row,
                0,
                "Total Oro Rosado 18K"
            )

            sheet.write_number(
                row,
                1,
                total_gramos_oro_rosado_18k,
                weight
            )

            row += 1

            # -------------------------------------
            # COBROS
            # -------------------------------------

            sheet.write(
                row,
                0,
                "Total Cobro Interno"
            )

            sheet.write_number(
                row,
                1,
                total_ci_local,
                money
            )

            row += 1

            sheet.write(
                row,
                0,
                "Total Hechura"
            )

            sheet.write_number(
                row,
                1,
                total_he_local,
                money
            )

            row += 1

            sheet.write(
                row,
                0,
                "Total Cobros Extras"
            )

            sheet.write_number(
                row,
                1,
                total_ce_local,
                money
            )

            row += 1

            sheet.write(
                row,
                0,
                "TOTAL PAGO A TALLER",
                total_format
            )

            sheet.write_number(
                row,
                1,
                total_pago_local,
                total_format
            )

            row += 3

            # =====================================
            # AGRUPAR POR MES
            # =====================================

            groups = OrderedDict()

            for r in sorted(
                store_recs,
                key=lambda x: x.fecha_firma
            ):

                dt = r.fecha_firma
                key = (dt.year, dt.month)

                groups.setdefault(key, []).append(r)

            # =====================================
            # DETALLE POR MES
            # =====================================

            for (year, month), month_recs in groups.items():

                sheet.write(
                    row,
                    0,
                    f"Periodo: {month:02d}/{year}",
                    bold
                )

                row += 1

                for col, h in enumerate(headers):
                    sheet.write(
                        row,
                        col,
                        h,
                        bold
                    )

                row += 1

                tot_gramos = 0
                tot_ci = 0
                tot_he = 0
                tot_ce = 0
                tot_pago = 0

                for r in month_recs:

                    gramos = getattr(
                        r,
                        'gramos_utilizado',
                        None
                    ) or getattr(
                        r,
                        'peso_total',
                        0
                    )

                    ci = r.cobro_interno or 0
                    he = r.hechura or 0
                    ce = r.cobros_extras or 0

                    pago = ci + he + ce

                    tot_gramos += gramos
                    tot_ci += ci
                    tot_he += he
                    tot_ce += ce
                    tot_pago += pago

                    sheet.write(
                        row,
                        0,
                        r.name or ""
                    )

                    if r.fecha_firma:
                        sheet.write_datetime(
                            row,
                            1,
                            r.fecha_firma,
                            datef
                        )

                    sheet.write(
                        row,
                        2,
                        r.metal_utilizado or ""
                    )

                    sheet.write_number(
                        row,
                        3,
                        gramos,
                        weight
                    )

                    sheet.write_number(
                        row,
                        4,
                        ci,
                        money
                    )

                    sheet.write_number(
                        row,
                        5,
                        he,
                        money
                    )

                    sheet.write_number(
                        row,
                        6,
                        ce,
                        money
                    )

                    sheet.write_number(
                        row,
                        7,
                        pago,
                        money
                    )

                    row += 1

                # ==========================
                # TOTAL DEL MES
                # ==========================

                sheet.write(
                    row,
                    0,
                    f"TOTAL MES {month:02d}/{year}",
                    total_format
                )

                sheet.write_number(
                    row,
                    3,
                    tot_gramos,
                    total_weight
                )

                sheet.write_number(
                    row,
                    4,
                    tot_ci,
                    total_format
                )

                sheet.write_number(
                    row,
                    5,
                    tot_he,
                    total_format
                )

                sheet.write_number(
                    row,
                    6,
                    tot_ce,
                    total_format
                )

                sheet.write_number(
                    row,
                    7,
                    tot_pago,
                    total_format
                )

                row += 3

            # =====================================
            # AJUSTAR COLUMNAS
            # =====================================

            sheet.set_column(0, 0, 25)
            sheet.set_column(1, 1, 18)
            sheet.set_column(2, 2, 20)
            sheet.set_column(3, 7, 18)
