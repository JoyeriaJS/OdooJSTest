{
    "name": "POS Discount Authorized",
    "version": "1.0",
    "summary": "Apply discounts in POS using authorization codes",
    "depends": ["point_of_sale"],
    "category": "Point of Sale",
    "data": [
        "security/ir.model.access.csv",
        "views/pos_discount_code_views.xml",
        "static/src/xml/product_screen.xml",
    ],
    "assets": {
        "point_of_sale.assets": [
            "pos_discount_authorized/static/src/js/discount_button.js",
            "pos_discount_authorized/static/src/xml/product_screen.xml",
        ],
    },
    "installable": True,
    "license": "LGPL-3",
}
