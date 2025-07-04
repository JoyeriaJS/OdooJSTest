from odoo import models, fields

class WizardSetPrecioOros(models.TransientModel):
    _name = 'wizard.set.precio.oros'
    _description = 'Valores de Oro para reporte'

    precio_oro_amarillo = fields.Float('Precio Oro Amarillo 18k', required=True, default=160000.0)
    precio_oro_rosado = fields.Float('Precio Oro Rosado 18k', required=True, default=150000.0)

    def action_print_report(self):
        # Aquí self.env.context['active_ids'] son los registros seleccionados
        return self.env.ref('joyeria_reparaciones.action_report_sales_by_store').report_action(
            self, data={
                'precio_oro_amarillo': self.precio_oro_amarillo,
                'precio_oro_rosado': self.precio_oro_rosado,
                'active_ids': self.env.context.get('active_ids', [])
            }
        )
