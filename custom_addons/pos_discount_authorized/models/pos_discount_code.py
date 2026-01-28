from odoo import models, fields, api
from datetime import timedelta
import pytz, random, string

class POSDiscountCode(models.Model):
    _name = "pos.discount.code"
    _description = "Código de descuento POS"

    code = fields.Char(readonly=True)
    discount_type = fields.Selection([
        ("percent", "Porcentaje"),
        ("amount", "Monto Fijo")
    ], default="amount")

    discount_value = fields.Float("Valor")
    used = fields.Boolean(default=False)
    expired = fields.Boolean(compute="_compute_expired", store=True)

    fecha_creacion = fields.Datetime(
        default=lambda self: fields.Datetime.now(),
        readonly=True
    )

    expiration_date = fields.Datetime(
        compute="_compute_expiration",
        store=True,
        readonly=True
    )

    fecha_uso = fields.Datetime()

    # ============================
    # GENERAR CÓDIGO
    # ============================
    @api.model
    def create(self, vals):
        vals["code"] = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )
        return super().create(vals)

    # ============================
    # EXPIRACIÓN AUTOMÁTICA (1 hora)
    # ============================
    @api.depends("fecha_creacion")
    def _compute_expiration(self):
        for rec in self:
            if rec.fecha_creacion:
                rec.expiration_date = rec.fecha_creacion + timedelta(hours=1)
            else:
                rec.expiration_date = False

    # ============================
    # MARCAR EXPIRADO
    # ============================
    @api.depends("expiration_date", "used")
    def _compute_expired(self):
        now = fields.Datetime.now()  # aware con TZ
        for record in self:

            if record.used:
                record.expired = True
                continue

            if not record.expiration_date:
                record.expired = False
                continue

            record.expired = record.expiration_date < now


