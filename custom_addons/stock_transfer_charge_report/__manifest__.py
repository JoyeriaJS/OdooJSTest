{
    'name': "Cargos entre Locales por Traspasos",
    'version': '1.0',
    'depends': ['stock', 'report'],
    'author': "Tu Empresa",
    'category': 'Inventory',
    'description': 'Reporte de cargos entre locales a través de traspasos internos',
    'data': [
        'report/stock_transfer_charge_report_action.xml',
        'report/stock_transfer_charge_report_templates.xml',
    ],
    'installable': True,
    'application': False,
}