from odoo import models, fields, api
import random
import string


class JoyeriaPosDiscount(models.Model):
    _name = 'joyeria.pos.discount'
    _description = 'Descuentos autorizados POS'

    name = fields.Char("Nombre", required=True)

    codigo = fields.Char(
        string="Código autorización",
        readonly=True,
        copy=False
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

    monto = fields.Float("Monto fijo")

    activo = fields.Boolean("Activo", default=True)

    usado = fields.Boolean("Usado", default=False)

    fecha_creacion = fields.Datetime(
        string="Fecha creación",
        default=fields.Datetime.now
    )

    def generar_codigo(self):
        for rec in self:
            codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            rec.codigo = codigo

    @api.model
    def crear_codigo(self, vals):
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        vals['codigo'] = codigo
        return super().create(vals)