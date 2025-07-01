{
    'name': 'Stock Transfer Charge Report Fixed',
    'version': '1.0',
    'category': 'Stock',
    'summary': 'Reporte de cobros entre locales',
    'depends': ['stock'],
    'data': [
        'report/stock_transfer_charge_report_action.xml',
        'report/stock_transfer_charge_report_templates.xml',
    ],
    'installable': True,
    'application': False,
}