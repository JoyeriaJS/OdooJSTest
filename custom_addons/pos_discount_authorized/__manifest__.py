
{
    "name": "POS Discount Authorized",
    "version": "1.0",
    "author": "ChatGPT",
    "depends": ["point_of_sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/pos_discount_views.xml",
        "static/src/xml/discount_assets.xml"
    ],
    "assets": {
        "point_of_sale.assets": [
            "pos_discount_authorized/static/src/js/discount_code.js"
        ]
    },
    "installable": true
}
