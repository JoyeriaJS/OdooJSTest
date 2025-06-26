{
    'name': 'POS & Reparaciones Report',
    'version': '17.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Reporte combinado de ventas POS y RMA',
    'depends': ['point_of_sale', 'joyeria_reparaciones'],
    'data': [
        'views/pos_jr_menu.xml',
        'views/report_pos_jr_template.xml',
    ],
    'installable': True,
    'application': False,
}
