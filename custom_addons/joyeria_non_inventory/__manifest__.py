{
    "name": "Productos No Inventariados",
    "version": "1.0",
    "summary": "Registro interno de productos no inventariados para control en Joyería",
    "category": "Inventory",
    "depends": ["base", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/non_inventory_views.xml",
        "views/menu.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}
