{
    "name": "POS Authorized Discount",
    "version": "1.0",
    "category": "Point of Sale",
    "summary": "Permite aplicar descuentos mediante códigos autorizados generados por el administrador.",
    "author": "JoyeríaJS",
    "website": "",
    "depends": ["base", "point_of_sale"],
    "data": [
        "views/discount_code_views.xml",
    ],
    "assets": {
        "point_of_sale.assets": [
            "pos_discount_authorized/static/src/js/pos_authorized_discount.js",
        ],
    },
    "installable": True,
    "application": False,
}
