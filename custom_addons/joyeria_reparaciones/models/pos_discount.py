from odoo import models, fields, api
import random
import string

class PosDiscount(models.Model):
    _name = 'joyeria.pos.discount'
    _description = 'Descuentos autorizados POS'

    name = fields.Char(string="Código", readonly=True)
    tipo_descuento = fields.Selection([
        ('porcentaje', 'Porcentaje'),
        ('monto', 'Monto Fijo')
    ], string="Tipo de descuento", required=True)

    porcentaje = fields.Selection([
        ('5', '5%'),
        ('10', '10%'),
        ('15', '15%')
    ], string="Porcentaje")

    monto = fields.Float(string="Monto fijo")

    activo = fields.Boolean(default=True)
    usado = fields.Boolean(default=False)

    fecha_creacion = fields.Datetime(default=fields.Datetime.now)

    @api.model
    def create(self, vals):
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        vals['name'] = codigo
        return super().create(vals)