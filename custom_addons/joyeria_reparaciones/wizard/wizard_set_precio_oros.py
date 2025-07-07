from odoo import models, fields, api

class WizardSetPrecioOros(models.TransientModel):
    _name = 'wizard.set.precio.oros'
    _description = 'Set precios de oro para reporte'

    precio_oro_amarillo = fields.Float("Oro Amarillo 18k", required=True)
    precio_oro_rosado   = fields.Float("Oro Rosado 18k", required=True)

    def print_report(self):
        # Valores del wizard
        data = {
            'precio_oro_amarillo': self.precio_oro_amarillo,
            'precio_oro_rosado': self.precio_oro_rosado,
        }
        # Obtener los IDs seleccionados (registros activos)
        docids = self.env.context.get('active_ids', [])
        return self.env.ref('joyeria_reparaciones.wizard_set_precio_oros_form').report_action(
            self.env['joyeria.reparacion'].browse(docids), data=data
        )