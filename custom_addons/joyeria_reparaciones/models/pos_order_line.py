from odoo import models, fields, api


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    gramos = fields.Char(string="Gramos")
    descripcion_personalizada = fields.Char(string="Descripción Personalizada")

    @api.model
    def _order_line_fields(self, line, session_id=None):
        result = super()._order_line_fields(line, session_id)
        result['gramos'] = line.get('gramos')
        result['descripcion_personalizada'] = line.get('descripcion_personalizada')
        return result