from odoo import models, fields

class PosSession(models.Model):
    _inherit = 'pos.session'
    vendedora_id = fields.Many2one('joyeria.vendedora', string='Vendedora')
