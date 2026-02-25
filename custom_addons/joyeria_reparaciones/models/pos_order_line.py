from odoo import models, fields, api


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    gramos = fields.Char(string="Gramos")
    descripcion_personalizada = fields.Char(string="Descripción Personalizada")

    @api.model
    def _order_line_fields(self, line, session_id=None):
        result = super()._order_line_fields(line, session_id)

        # 🔥 En Odoo 17 la línea viene como lista [0, 0, values]
        if isinstance(line, (list, tuple)) and len(line) > 2:
            values = line[2]
        else:
            values = line

        result['gramos'] = values.get('gramos')
        result['descripcion_personalizada'] = values.get('descripcion_personalizada')

        return result