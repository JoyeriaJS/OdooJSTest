from odoo import models, fields, api
import random
import string


class JoyeriaPosDiscount(models.Model):
    _name = 'joyeria.pos.discount'
    _description = 'Codigos de descuento POS'

    name = fields.Char("Nombre", required=True)

    tipo_descuento = fields.Selection([
        ('porcentaje', 'Porcentaje'),
        ('monto', 'Monto fijo')
    ], string="Tipo de descuento", required=True)

    porcentaje = fields.Selection([
        ('5', '5%'),
        ('10', '10%'),
        ('15', '15%')
    ], string="Porcentaje")

    monto = fields.Float("Monto fijo")
    

    codigo = fields.Char(
        "Código autorización",
        readonly=True,
        copy=False
    )

    activo = fields.Boolean(default=True)
    usado = fields.Boolean("Usado", default=False)

    @api.model
    def create(self, vals):
        if not vals.get('codigo'):
            vals['codigo'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return super().create(vals)