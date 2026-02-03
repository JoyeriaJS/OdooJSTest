{
    "name": "POS Discount Authorized",
    "version": "1.0",
    "category": "Point of Sale",
    "summary": "Requiere código para aplicar descuentos en POS",
    "depends": ["point_of_sale"],
    "data": [
        "views/pos_authcode_views.xml",

        
    ],
    "assets": {
        "point_of_sale.assets_prod": [
            "pos_discount_authorized/static/src/js/discount_hook.js",
            "pos_discount_authorized/static/src/xml/discount_popup.xml",
        ]
    },
    "installable": True,
    "license": "LGPL-3",
}
