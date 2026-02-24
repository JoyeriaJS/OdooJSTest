from odoo import models

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        result.append('joyeria.vendedora')
        return result

    def _loader_params_joyeria_vendedora(self):
        return {
            'search_params': {
                'domain': [],
                'fields': ['name', 'codigo_qr'],
            },
        }

    def _get_pos_ui_joyeria_vendedora(self, params):
        return self.env['joyeria.vendedora'].search_read(**params['search_params'])