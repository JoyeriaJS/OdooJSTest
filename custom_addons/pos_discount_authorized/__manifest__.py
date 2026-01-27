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
        "point_of_sale.assets": [
            "pos_discount_authorized/static/src/js/discount_override.js",
        ]
    },
    "installable": True,
    "application": False,
}
