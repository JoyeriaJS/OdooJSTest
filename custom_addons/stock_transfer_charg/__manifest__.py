{
    'name': 'Stock Transfer Charges Report',
    'version': '1.0',
    'category': 'Reporting',
    'summary': 'Reporte de cobros entre locales basado en traspasos de inventario',
    'depends': ['stock', 'joyeria_reparaciones'],
    'data': [
        'report/stock_transfer_report.xml',
        'report/stock_transfer_report_template.xml',
    ],
    'installable': True,
    'application': False,
}
