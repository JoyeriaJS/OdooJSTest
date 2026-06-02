from odoo import models, fields, api
import base64
import qrcode

from io import BytesIO


class JoyeriaCotizacion(models.Model):
    _name = "joyeria.cotizacion"
    _description = "Cotizacion Joyeria"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "name"

    name = fields.Char(
        string="Numero",
        required=True,
        readonly=True,
        copy=False,
        default="Nuevo"
    )

    partner_id = fields.Many2one(
        "res.partner",
        string="Cliente",
        required=True,
        tracking=True
    )

    email = fields.Char(
        string="Correo"
    )

    telefono = fields.Char(
        string="Telefono"
    )

    direccion = fields.Char(
        string="Direccion"
    )

    fecha = fields.Date(
        default=fields.Date.today
    )

    fecha_vencimiento = fields.Date()

    estado = fields.Selection([
        ("borrador", "Borrador"),
        ("enviada", "Enviada"),
        ("aceptada", "Aceptada"),
        ("rechazada", "Rechazada"),
    ], default="borrador", tracking=True)

    line_ids = fields.One2many(
        "joyeria.cotizacion.line",
        "cotizacion_id",
        string="Lineas"
    )

    total = fields.Float(
        compute="_compute_total",
        store=True
    )

    qr_code = fields.Binary(
        string="QR",
        readonly=True
    )

    @api.depends("line_ids.subtotal")
    def _compute_total(self):
        for rec in self:
            rec.total = sum(
                rec.line_ids.mapped("subtotal")
            )

    @api.model
    def create(self, vals):

        if vals.get("name", "Nuevo") == "Nuevo":
            vals["name"] = self.env[
                "ir.sequence"
            ].next_by_code(
                "joyeria.cotizacion"
            )

        rec = super().create(vals)

        rec.generar_qr()

        return rec

    def write(self, vals):

        res = super().write(vals)

        self.generar_qr()

        return res

    def generar_qr(self):

        for rec in self:

            qr = qrcode.make(
                rec.name or ""
            )

            buffer = BytesIO()

            qr.save(
                buffer,
                format="PNG"
            )

            rec.qr_code = base64.b64encode(
                buffer.getvalue()
            )

    def action_borrador(self):
        self.estado = "borrador"

    def action_enviada(self):
        self.estado = "enviada"

    def action_aceptada(self):
        self.estado = "aceptada"

    def action_rechazada(self):
        self.estado = "rechazada"