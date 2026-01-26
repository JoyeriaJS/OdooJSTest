{
    "name": "POS Discount Authorized",
    "version": "1.0",
    "depends": ["point_of_sale"],
    "data": [
        "security/pos_discount_model.xml",
        "security/ir.model.access.csv",
        "models/pos_discount_code_model.xml",
        "views/discount_code_views.xml",
    ],
    "assets": {
    "point_of_sale.assets_prod": [
        "pos_discount_authorized/static/src/js/discount_code.js",
        "pos_discount_authorized/static/src/xml/discount_button.xml"
    ],
    "point_of_sale.assets_debug": [
        "pos_discount_authorized/static/src/js/discount_code.js",
        "pos_discount_authorized/static/src/xml/discount_button.xml"
    ]
    },
    "installable": True,
}
