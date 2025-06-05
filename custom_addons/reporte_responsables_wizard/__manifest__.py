{
    "name": "Reporte Responsables Wizard",
    "version": "16.0.1.0.0",
    "category": "Custom",
    "summary": "Reporte PDF de órdenes de reparación por responsable y rango de fechas dinámico.",
    "author": "Dante & ChatGPT",
    "depends": ["base", "joyeria_reparacion"],  # Cambia "joyeria_reparacion" por el nombre real de tu módulo base si es necesario
    "data": [
        "security/ir.model.access.csv",
        "views/wizard_view.xml",
        "views/responsables_button.xml",
        "report/reporte_responsables_report.xml",
        "report/reporte_responsables_template.xml"
    ],
    "application": False,
    "installable": True
}
