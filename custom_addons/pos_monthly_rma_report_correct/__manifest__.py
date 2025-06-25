# -*- coding: utf-8 -*-
{
    "name": "Reporte Mensual RMA + POS",
    "version": "1.0.2",
    "author": "Joyería Sebastián",
    "category": "Point of Sale",
    "license": "AGPL-3",
    "depends": ["point_of_sale", "joyeria_reparaciones"],
    "data": [
        "report/rma_monthly_report_action.xml",
        "report/rma_monthly_template.xml",
        "views/menu_rma_monthly.xml"
    ],
    "installable": True,
    "application": False
}
