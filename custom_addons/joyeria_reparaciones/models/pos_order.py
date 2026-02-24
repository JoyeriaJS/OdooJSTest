from odoo import models, fields, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    vendedora_id = fields.Many2one(
        'joyeria.vendedora',
        string='Vendedora'
    )

    @api.model
    def _order_fields(self, ui_order):
        result = super()._order_fields(ui_order)
        result['vendedora_id'] = ui_order.get('vendedora_id')
        return result

    def export_for_ui(self):
        result = super().export_for_ui()

        for order in result:
            pos_order = self.browse(order['id'])
            order['vendedora_name'] = pos_order.vendedora_id.name if pos_order.vendedora_id else ""

        return result