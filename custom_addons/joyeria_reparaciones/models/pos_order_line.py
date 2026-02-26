from odoo import models, fields, api


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    gramos = fields.Char(string="Gramos")
    descripcion_personalizada = fields.Char(string="Descripción Personalizada")

    @api.model
    def _order_line_fields(self, line, session_id=None):
        result = super()._order_line_fields(line, session_id)

        # 🔥 Solo si viene en formato ORM estándar
        if isinstance(line, (list, tuple)) and len(line) >= 3:
            values = line[2]
            if isinstance(values, dict):
                result.update({
                    'gramos': values.get('gramos'),
                    'descripcion_personalizada': values.get('descripcion_personalizada'),
                })

        return result