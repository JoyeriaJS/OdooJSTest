{
    'name': 'pos_qr_auth_no_wizard',
    'version': '1.0',
    'author': 'Joyería Sebastián',
    'category': 'Point of Sale',
    'license': 'AGPL-3',
    'depends': ['point_of_sale', 'joyeria_reparaciones'],
    'data': [
        'security/ir.model.access.csv',
        'report/report_rma_pos.xml',
        'views/pos_qr_auth_views.xml',
        'views/pos_qr_auth_menu.xml',
    ],
    'assets': {
        'point_of_sale.assets_backend': [
            'pos_qr_auth_no_wizard/static/src/js/qr_auth.js',
        ],
    },
    'installable': True,
    'application': False,
}