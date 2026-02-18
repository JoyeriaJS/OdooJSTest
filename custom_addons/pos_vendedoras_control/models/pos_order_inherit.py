from odoo import models, api


class PosOrderInherit(models.Model):
    _inherit = 'pos.order'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            args += ['|', ('name', operator, name), ('pos_reference', operator, name)]
        return self.search(args, limit=limit).name_get()
