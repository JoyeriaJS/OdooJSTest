# -*- coding: utf-8 -*-
{
    'name': 'pos_daily_rma_report',
    'version': '1.0',
    'author': 'Joyería Sebastián',
    'category': 'Point of Sale',
    'license': 'AGPL-3',
    'depends': ['point_of_sale', 'joyeria_reparaciones'],
    'data': [
        'security/ir.model.access.csv',
        'views/pos_daily_rma_report_wizard_view.xml',
        'report/pos_daily_rma_report_template.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
}
