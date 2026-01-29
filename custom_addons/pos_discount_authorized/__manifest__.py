{
    "name": "POS Discount Authorized",
    "version": "1.0",
    "depends": ["point_of_sale"],
    "assets": {
        "point_of_sale.assets": [
            "pos_discount_authorized/static/src/js/discount_button.js",
            "pos_discount_authorized/static/src/xml/discount_button.xml",
        ],
    },
    "data": [
        "views/pos_discount_code_views.xml",
        
    ],
    "installable": True,
}
