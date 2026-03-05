from odoo import models, fields, api
import random
import string


class JoyeriaPosDiscount(models.Model):
    _name = 'joyeria.pos.discount'
    _description = 'Codigos de descuento POS'

    name = fields.Char("Código", required=True, copy=False, default="Nuevo")
    tipo = fields.Selection([
        ('porcentaje', 'Porcentaje'),
        ('monto', 'Monto fijo')
    ], string="Tipo", required=True)

    porcentaje = fields.Selection([
        ('5', '5%'),
        ('10', '10%'),
        ('15', '15%')
    ], string="Porcentaje")

    monto = fields.Float("Monto fijo")

    activo = fields.Boolean("Activo", default=True)

    usado = fields.Boolean("Usado", default=False)

    fecha_creacion = fields.Datetime(
        "Fecha creación",
        default=fields.Datetime.now
    )

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            vals['name'] = codigo
        return super().create(vals)