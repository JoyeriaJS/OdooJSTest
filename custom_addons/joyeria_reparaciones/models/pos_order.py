from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PosOrder(models.Model):
    _inherit = 'pos.order'

    vendedora_id = fields.Many2one(
        'joyeria.vendedora',
        string='Vendedora'
    )

    codigo_qr_vendedora = fields.Char(
        string='Código QR Vendedora'
    )

    @api.model
    def _order_fields(self, ui_order):
        result = super()._order_fields(ui_order)

        codigo = ui_order.get('codigo_qr_vendedora')

        if not codigo:
            raise ValidationError("Debe escanear o ingresar el código de la vendedora.")

        codigo = str(codigo).strip().upper()

        vendedora = self.env['joyeria.vendedora'].search([
            '|', '|',
            ('clave_autenticacion', '=', codigo),
            ('clave_qr', '=', codigo),
            ('codigo_qr', '=', codigo),
        ], limit=1)

        if not vendedora:
            raise ValidationError("QR o código de vendedora inválido.")

        result['vendedora_id'] = vendedora.id
        result['codigo_qr_vendedora'] = codigo

        return result