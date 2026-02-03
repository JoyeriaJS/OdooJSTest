{
    "name": "POS Discount Authorized",
    "version": "17.0.1.0.0",
    "category": "Point of Sale",
    "depends": ["point_of_sale"],
    "data": [
        "views/pos_auth_code_views.xml",
        "security/ir.model.access.csv",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_discount_authorized/static/src/js/discount_hook.js",
        ],
    },
    "installable": True,
    "license": "LGPL-3"
}
