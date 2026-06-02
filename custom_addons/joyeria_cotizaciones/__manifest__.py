{
    "name": "Joyeria Cotizaciones",
    "version": "17.0.1.0.0",
    "category": "Sales",
    "summary": "Cotizaciones independientes para joyería",
    "author": "Joyeria Sebastian",
    "license": "LGPL-3",
    "depends": [
        "base",
        "mail",
        "contacts",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/cotizacion_views.xml",
        "data/sequence.xml",
        "report/cotizacion_report.xml",
        "report/cotizacion_template.xml",
    ],
    "installable": True,
    "application": True,
}