from odoo import models, fields

class PosOrder(models.Model):
    _inherit = 'pos.order'
    vendedora_id = fields.Many2one('joyeria.vendedora', string='Vendedora', related='session_id.vendedora_id', store=True)
