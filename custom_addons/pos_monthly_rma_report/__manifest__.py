{
    "name": "Reporte Mensual RMA + POS",
    "version": "1.0",
    "category": "Point of Sale",
    "summary": "Reporte mensual que suma reparaciones (RMA) y ventas POS por mes",
    "depends": ["point_of_sale", "joyeria_reparaciones"],
    "data": [
        "report/report_rma_monthly_action.xml",
        "report/rma_monthly_template.xml",
        "views/menu_rma_monthly.xml"
    ],
    "installable": true,
    "application": false
}
