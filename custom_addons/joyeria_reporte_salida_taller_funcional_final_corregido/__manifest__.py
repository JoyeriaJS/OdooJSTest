{
    "name": "Reporte Salida Taller Funcional",
    "version": "1.0",
    "depends": ["base"],
    "author": "Asistente Odoo",
    "category": "Reportes",
    "description": "Reporte agrupado por mes y año de salida del taller",
    "data": [
        "security/ir.model.access.csv",
        "views/menu_salida_taller.xml",
        "report/salida_taller_template.xml",
        "report/salida_taller_report.xml"
    ],
    "installable": True,
    "application": True
}