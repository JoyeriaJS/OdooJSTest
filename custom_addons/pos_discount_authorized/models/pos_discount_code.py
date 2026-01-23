
from odoo import models, fields, api
from datetime import datetime, timedelta
import pytz, random, string

class POSDiscountCode(models.Model):
    _name = "pos.discount.code"
    _description = "Código de descuento POS"

    code = fields.Char(readonly=True)
    discount_type = fields.Selection([("percent", "Porcentaje"), ("fixed", "Monto Fijo")], default="fixed")
    discount_value = fields.Float("Valor")
    used = fields.Boolean(default=False)
    expired = fields.Boolean(compute="_compute_expired", store=True)
    fecha_uso = fields.Datetime()

    @api.model
    def create(self, vals):
        vals["code"] = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return super().create(vals)

    @api.depends("create_date", "used")
    def _compute_expired(self):
        for rec in self:
            if rec.used:
                rec.expired = True
                continue
            if not rec.create_date:
                rec.expired = False
                continue
            now=datetime.now(pytz.UTC)
            rec.expired = rec.create_date + timedelta(hours=1) <= now
