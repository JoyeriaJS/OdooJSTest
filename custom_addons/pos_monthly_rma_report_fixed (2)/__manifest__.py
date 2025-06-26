{
    'name': 'Reporte Mensual RMA + POS',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'Reporte mensual de ventas POS y RMA',
    'depends': ['point_of_sale', 'joyeria_reparaciones'],
    'data': [
        'report/report.xml',
        'report/rma_monthly_template.xml',
        'views/menu_rma_monthly.xml',
    ],
    'installable': True,
    'application': False,
}
