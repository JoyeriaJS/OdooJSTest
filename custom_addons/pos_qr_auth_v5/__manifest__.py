{
    'name': 'POS QR Auth',
    'version': '1.3',
    'author': 'Joyería Sebastián',
    'category': 'Point of Sale',
    'license': 'AGPL-3',
    'depends': ['point_of_sale', 'joyeria_reparaciones'],
    'data': [
        'security/ir.model.access.csv',
        'views/pos_qr_auth_views.xml',
        'views/rma_pos_report_wizard_view.xml',
        'views/report_rma_pos.xml',
    ],
    'assets': {
        'point_of_sale.assets_backend': [
            'pos_qr_auth/static/src/js/qr_auth.js',
        ],
    },
    'installable': True,
    'application': False,
}