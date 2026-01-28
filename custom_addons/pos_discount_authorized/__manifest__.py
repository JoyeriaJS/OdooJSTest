{
    "name": "POS Discount Authorized",
    "version": "1.0",
    "summary": "Descuentos autorizados por código en el POS",
    "author": "Sebastián Joyería",
    "depends": ["point_of_sale"],
    "data": [
        "security/pos_discount_rule.xml",
        "security/ir.model.access.csv",
        "views/pos_discount_code_views.xml"
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_discount_authorized/static/src/js/discount_button.js",
            "pos_discount_authorized/static/src/xml/discount_button.xml"
        ]
    },
    "installable": True,
    "application": False
}
