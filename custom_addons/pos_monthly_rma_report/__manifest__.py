# -*- coding: utf-8 -*-
{
    'name': 'Reporte Mensual RMA + POS',
    'version': '1.0.0',
    'author': 'Joyería Sebastián',
    'category': 'Point of Sale',
    'license': 'AGPL-3',
    'depends': ['point_of_sale', 'joyeria_reparaciones'],
    'data': [
        'report/report_monthly_rma_pos.xml',
        'report/template_monthly_rma_pos.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
}
