
{
    "name": "POS Discount Authorized",
    "version": "1.0",
    "author": "Dante",
    "depends": ["point_of_sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/pos_discount_code_views.xml"
    ],
    "assets": {
        "point_of_sale.assets": [
            "pos_discount_authorized/static/src/js/discount_button.js",
            "pos_discount_authorized/static/src/xml/discount_button.xml",
        ],
        
    "installable": True,
}
 }