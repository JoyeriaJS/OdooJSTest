{
    "name": "POS Discount Authorized",
    "version": "1.0",
    "summary": "Autoriza descuentos en POS mediante códigos",
    "depends": ["point_of_sale"],
    "data": [
        "views/pos_auth_code_views.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_discount_authorized/static/src/js/discount_hook.js",
            "pos_discount_authorized/static/src/xml/discount_popup.xml",
        ],
    },
    "post_load": "static/src/js/discount_hook.js",
    "installable": True,
    "license": "LGPL-3",
    
}
