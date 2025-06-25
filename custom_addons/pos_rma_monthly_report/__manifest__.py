# -*- coding: utf-8 -*-
{
    'name': 'Reporte Mensual RMA + POS',
    'version': '1.0.3',
    'author': 'Joyería Sebastián',
    'category': 'Point of Sale',
    'license': 'AGPL-3',
    'depends': ['point_of_sale', 'joyeria_reparaciones'],
    'data': [
        'views/menu_rma_monthly.xml',
        'report/report_rma_monthly.xml',
        'report/template_rma_monthly.xml',
    ],
    'installable': True,
    'application': False,
}
