# models/confirm_reparacion_wizard.py
from odoo import api, fields, models

class ConfirmReparacionWizard(models.TransientModel):
    _name = 'confirm.reparacion.wizard'
    _description = 'Confirmar creación de RMA'

    # Almacenamos los valores que vienen de contexto
    default_vals = fields.Serialized(string="Valores por defecto")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        # Cargamos en el wizard el dict de vals
        res['default_vals'] = self.env.context.get('default_vals') or {}
        return res

    def action_confirm(self):
        """El usuario dijo SÍ, creamos la orden usando los vals."""
        vals = self.default_vals or {}
        self.env['joyeria.reparacion'].with_context(_confirming_rma=True).create(vals)
        return {'type': 'ir.actions.act_window_close'}

    def action_cancel(self):
        """El usuario dijo NO: simplemente cerramos."""
        return {'type': 'ir.actions.act_window_close'}
