{
    'name': 'Joyeria Reparaciones DEMO',
    'version': '1.0',
    'summary': 'Demo: Reporte PDF con Wizard y External ID',
    'author': 'DR + ChatGPT',
    'depends': ['base'],
    'data': [
        'views/reparacion_views.xml',
        'report/report_sales_by_store.xml',
        'report/report_sales_by_store_template.xml',
        'wizard/wizard_set_precio_oros_view.xml',
        'wizard/wizard_set_precio_oros_action.xml',
    ],
    'application': True,
}
