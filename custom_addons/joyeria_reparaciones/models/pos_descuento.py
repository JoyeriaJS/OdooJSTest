from odoo import models, fields, api
from datetime import datetime


class PosDescuentoAutorizado(models.Model):
    _name = "pos.descuento.autorizado"
    _description = "Descuentos autorizados POS"

    name = fields.Char("Código")
    tipo = fields.Selection([
        ('porcentaje', 'Porcentaje'),
        ('monto', 'Monto fijo')
    ])

    valor = fields.Float("Valor")

    activo = fields.Boolean(default=True)

    fecha_expiracion = fields.Datetime()

    producto_descuento_id = fields.Many2one(
        'product.product',
        string="Producto descuento"
    )

    @api.model
    def validar_codigo_pos(self, codigo):

        descuento = self.search([
            ('name', '=', codigo),
            ('activo', '=', True)
        ], limit=1)

        if not descuento:
            return False

        if descuento.fecha_expiracion and descuento.fecha_expiracion < fields.Datetime.now():
            return False

        return {
            "tipo": descuento.tipo,
            "valor": descuento.valor,
            "producto_descuento_id": descuento.producto_descuento_id.id
        }