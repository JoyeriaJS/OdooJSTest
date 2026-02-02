{
    "name": "POS Discount Authorized",
    "version": "17.0.1.0.0",
    "depends": ["point_of_sale"],
    "category": "Point of Sale",
    "author": "Joyería Sebastián",
    "license": "LGPL-3",
    "installable": True,

    "assets": {
        "point_of_sale._assets_pos_frontend": [
            "pos_discount_authorized/static/src/js/discount_pos.js",
            "pos_discount_authorized/static/src/xml/discount_popup.xml",
        ],
    },
}
