# -*- coding: utf-8 -*-
{
    'name': 'Reporte Mensual RMA + POS',
    'version': '1.0.0',
    'author': 'Joyería Sebastián',
    'category': 'Point of Sale',
    'license': 'AGPL-3',
    'depends': ['point_of_sale', 'joyeria_reparaciones'],
    'data': [
        'report/report_rma_monthly.xml',
        'report/template_rma_monthly.xml',
        'views/menu_rma_monthly.xml'
    ],
    'installable': True,
    'application': False,
}
