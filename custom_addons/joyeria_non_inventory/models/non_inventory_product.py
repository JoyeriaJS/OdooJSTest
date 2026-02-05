from odoo import models, fields

class NonInventoryProduct(models.Model):
    _name = "joyeria.non_inventory_product"
    _description = "Producto no inventariado"
    _order = "fecha desc"

    fecha = fields.Datetime(
        string="Fecha de registro",
        default=lambda self: fields.Datetime.now(),
        readonly=True
    )

    user_id = fields.Many2one(
        "res.users",
        string="Registrado por",
        default=lambda self: self.env.user,
        readonly=True
    )

    descripcion = fields.Char("Descripción del producto", required=True)

    peso = fields.Float("Peso (gr)", digits=(6,3))

    metal = fields.Selection([
        ("oro", "Oro"),
        ("plata", "Plata"),
        ("acero", "Acero"),
        ("fantasia", "Fantasía"),
        ("otro", "Otro"),
    ], string="Metal")

    sucursal_id = fields.Many2one(
        "stock.warehouse",
        string="Sucursal"
    )

    foto = fields.Binary("Foto del producto")

    observaciones = fields.Text("Observaciones")

    codigo_interno = fields.Char("Código interno")

    estado = fields.Selection([
        ("pendiente", "Pendiente"),
        ("regularizado", "Regularizado"),
        ("descartado", "Descartado")
    ], string="Estado", default="pendiente")
