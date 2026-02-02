{
    "name": "POS Authorized Discount",
    "version": "1.0",
    "author": "Joyería Sebastián",
    "depends": ["point_of_sale"],
    "data": [
        "views/discount_code_views.xml",
    ],
    "assets": {
        "point_of_sale.assets": [
            "pos_discount_authorized/static/src/js/discount_pos.js",
        ],
    },
    "installable": True,
}
