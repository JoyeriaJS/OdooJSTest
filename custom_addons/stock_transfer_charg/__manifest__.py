{
    'name': 'Stock Transfer Charges Report',
    'version': '1.0',
    'category': 'Reporting',
    'summary': 'Reporte de cobros entre locales basado en traspasos de inventario',
    'depends': ['stock', 'joyeria_reparaciones'],
    'data': [
        'report/stock_transfer_charge_report_action.xml',
        'report/stock_transfer_charge_report_templates.xml',
    ],
    'installable': True,
    'application': False,
}
