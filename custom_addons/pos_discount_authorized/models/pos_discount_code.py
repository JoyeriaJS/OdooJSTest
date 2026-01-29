from odoo import models, fields, api
from datetime import timedelta
import random, string

class POSDiscountCode(models.Model):
    _name = "pos.discount.code"
    _description = "Authorized POS Discount Code"

    code = fields.Char(readonly=True)
    discount_type = fields.Selection(
        [("percent", "Percentage"), ("amount", "Fixed Amount")],
        default="percent"
    )
    discount_value = fields.Float("Value")
    used = fields.Boolean(default=False)
    fecha_creacion = fields.Datetime(default=lambda self: fields.Datetime.now())
    expiration_date = fields.Datetime(compute="_compute_expiration", store=True)
    expired = fields.Boolean(compute="_compute_expired", store=True)

    def create(self, vals):
        vals["code"] = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return super().create(vals)

    @api.depends("fecha_creacion")
    def _compute_expiration(self):
        for rec in self:
            rec.expiration_date = rec.fecha_creacion + timedelta(hours=1)

    @api.depends("expiration_date", "used")
    def _compute_expired(self):
        now = fields.Datetime.now()
        for rec in self:
            rec.expired = rec.used or (rec.expiration_date < now)

    def action_mark_used(self):
        for rec in self:
            rec.used = True

    @api.model
    def validate_code(self, code):
        rec = self.search([("code", "=", code)], limit=1)
        if not rec:
            return {"valid": False, "message": "No existe el código."}

        if rec.used:
            return {"valid": False, "message": "El código ya fue utilizado."}

        if rec.expired:
            return {"valid": False, "message": "El código ha expirado."}

        rec.used = True

        return {
            "valid": True,
            "type": rec.discount_type,
            "value": rec.discount_value,
            "product_id": 1,  # ID de producto descuento genérico
        }