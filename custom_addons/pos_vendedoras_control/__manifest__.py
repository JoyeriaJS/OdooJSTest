{
    'name': 'Control Ventas por Vendedora POS',
    'version': '17.0.1.0.0',
    'summary': 'Control de ventas netas por vendedora con gastos',
    'author': 'JS',
    'category': 'Point of Sale',
    'depends': ['point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/venta_vendedora_views.xml',
    ],
    'installable': True,
    'application': True,
}
