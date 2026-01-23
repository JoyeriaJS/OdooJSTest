
{
    "name": "POS Discount Authorized",
    "version": "1.0",
    "depends": ["point_of_sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/discount_code_views.xml",
        "views/discount_button_template.xml"
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "/pos_discount_authorized/static/src/js/discount_code.js"
        ]
    },
    "installable": True
}
