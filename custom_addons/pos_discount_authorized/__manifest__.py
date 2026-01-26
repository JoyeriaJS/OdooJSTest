{
    "name": "POS Discount Authorized",
    "version": "1.0",
    "depends": ["point_of_sale"],
    "data": [
        "security/pos_discount_model.xml",
        "security/ir.model.access.csv",
        "models/pos_discount_code_model.xml",
        "views/discount_code_views.xml"
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_discount_authorized/static/src/js/discount_code.js",
            "pos_discount_authorized/static/src/xml/discount_button.xml",
            "pos_discount_authorized/static/src/js/override_discount_button.js",
        ]
    },
    "installable": True,
    "application": False
}
