from odoo import models, fields, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    vendedora_id = fields.Many2one('joyeria.vendedora')
    codigo_qr_vendedora = fields.Char()

    @api.model
    def _order_fields(self, ui_order):

        # Siempre obtener resultado del super
        result = super()._order_fields(ui_order)

        # 🔒 Seguridad: si super devuelve None, lo convertimos en dict
        if not result:
            result = {}

        codigo = ui_order.get('codigo_qr_vendedora')

        if codigo:
            vendedora = self.env['joyeria.vendedora'].search(
                [('codigo_qr', '=', codigo.strip())],
                limit=1
            )

            if vendedora:
                result['vendedora_id'] = vendedora.id
                result['codigo_qr_vendedora'] = codigo

        return result