{
    'name': 'Monthly RMA and POS Report',
    'version': '15.0.1.0.0',
    'author': 'Custom',
    'category': 'Reporting',
    'depends': ['point_of_sale', 'joyeria_reparaciones'],
    'data': [
        'views/report_sales_by_store.xml',
        'views/report_sales_by_store_template.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
}