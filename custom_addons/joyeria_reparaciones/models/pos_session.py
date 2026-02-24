from odoo import models

class PosSession(models.Model):
    _inherit = 'pos.session'

    # 🔹 Agregamos el modelo joyeria.vendedora al POS
    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        result.append('joyeria.vendedora')
        return result

    # 🔹 Definimos qué campos del modelo se enviarán al POS
    def _loader_params_joyeria_vendedora(self):
        return {
            'search_params': {
                'domain': [],
                'fields': [
                    'name',
                    'codigo_qr',
                    'clave_qr',
                    'clave_autenticacion',
                ],
            },
        }

    # 🔹 Enviamos los registros al frontend
    def _get_pos_ui_joyeria_vendedora(self, params):
        return self.env['joyeria.vendedora'].search_read(
            **params['search_params']
        )