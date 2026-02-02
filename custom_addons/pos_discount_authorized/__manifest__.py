{
    "name": "POS Authorized Discount",
    "version": "1.0",
    "summary": "Adds a discount authorization button to POS",
    "depends": ["point_of_sale"],
    "category": "Point of Sale",
    "data": [
        "security/ir.model.access.csv",
        "views/pos_discount_code_views.xml",
    ],
    "assets": {
        "point_of_sale_.assets_pos": [
            "pos_discount_authorized/static/src/js/discount_button.js",
            "pos_discount_authorized/static/src/xml/product_screen.xml",
        ],
    },
    "installable": True,
    "license": "LGPL-3",
}
