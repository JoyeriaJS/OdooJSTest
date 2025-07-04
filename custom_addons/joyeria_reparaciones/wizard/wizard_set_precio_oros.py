from odoo import models, fields, api

class WizardSetPrecioOros(models.TransientModel):
    _name = 'wizard.set.precio.oros'
    _description = 'Set precios de oro para reporte'

    precio_oro_amarillo = fields.Float("Oro Amarillo 18k", required=True)
    precio_oro_rosado   = fields.Float("Oro Rosado 18k", required=True)

    def print_report(self):
        # Esta función genera el reporte usando los valores ingresados
        # Requiere que se le pase docids, por ejemplo con contexto o data.
        data = {
            'precio_oro_amarillo': self.precio_oro_amarillo,
            'precio_oro_rosado': self.precio_oro_rosado,
        }
        # Normalmente el wizard conoce los IDs a reportar a través del contexto
        docids = self.env.context.get('active_ids', [])
        return self.env.ref('joyeria_reparaciones.report_sales_by_store_template').report_action(docids, data=data)
