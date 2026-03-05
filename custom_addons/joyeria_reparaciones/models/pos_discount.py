from odoo import models, fields, api
import random
import string


class PosDiscount(models.Model):
    _name = "joyeria.pos.discount"
    _description = "Descuentos autorizados POS"

    name = fields.Char(
        string="Código",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self._generate_code()
    )

    tipo_descuento = fields.Selection([
        ('porcentaje', 'Porcentaje'),
        ('monto', 'Monto fijo')
    ], string="Tipo de descuento", required=True)

    porcentaje = fields.Selection([
        ('5', '5%'),
        ('10', '10%'),
        ('15', '15%')
    ], string="Porcentaje")

    monto = fields.Float(string="Monto fijo")

    activo = fields.Boolean(default=True)

    usado = fields.Boolean(default=False)

    fecha_creacion = fields.Datetime(
        string="Fecha creación",
        default=fields.Datetime.now
    )

    usuario_creador = fields.Many2one(
        'res.users',
        default=lambda self: self.env.user
    )

    # Generador automático de código
    def _generate_code(self):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return code