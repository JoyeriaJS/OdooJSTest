{
    'name': 'Monthly RMA + POS Report',
    'summary': 'Reporte mensual combinando RMA y POS',
    'version': '1.0',
    'category': 'Point of Sale',
    'author': 'ChatGPT',
    'depends': ['base', 'point_of_sale', 'joyeria_reparaciones'],
    'data': [
        'views/menu_rma_monthly.xml',
        'views/report_action.xml',
        'views/report_template.xml',
    ],
    'installable': True,
    'application': False,
}
