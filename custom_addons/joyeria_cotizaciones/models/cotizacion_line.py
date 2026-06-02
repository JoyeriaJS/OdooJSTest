from odoo import models, fields, api


class JoyeriaCotizacionLine(models.Model):
    _name = "joyeria.cotizacion.line"
    _description = "Linea Cotizacion"

    cotizacion_id = fields.Many2one(
        "joyeria.cotizacion",
        required=True,
        ondelete="cascade"
    )

    descripcion = fields.Char(
        required=True
    )

    cantidad = fields.Float(
        default=1
    )

    precio_unitario = fields.Float()

    subtotal = fields.Float(
        compute="_compute_subtotal",
        store=True
    )

    @api.depends(
        "cantidad",
        "precio_unitario"
    )
    def _compute_subtotal(self):

        for rec in self:

            rec.subtotal = (
                (rec.cantidad or 0)
                *
                (rec.precio_unitario or 0)
            )