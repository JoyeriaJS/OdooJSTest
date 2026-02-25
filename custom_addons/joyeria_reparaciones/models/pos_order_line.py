from odoo import models, fields, api


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    gramos = fields.Char(string="Gramos")
    descripcion_personalizada = fields.Char(string="Descripción Personalizada")

    @api.model
    def _order_line_fields(self, line, session_id=None):
        result = super()._order_line_fields(line, session_id)

        values = {}

        # Caso 1: viene como [0, 0, {...}]
        if isinstance(line, (list, tuple)):
            if len(line) >= 3 and isinstance(line[2], dict):
                values = line[2]

        # Caso 2: viene como dict directo
        elif isinstance(line, dict):
            values = line

        # Solo asignamos si realmente es dict
        if isinstance(values, dict):
            result['gramos'] = values.get('gramos', False)
            result['descripcion_personalizada'] = values.get('descripcion_personalizada', False)

        return result