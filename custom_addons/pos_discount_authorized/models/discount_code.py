from odoo import models, fields, api
from datetime import datetime

class PosAuthorizedDiscount(models.Model):
    _name = "pos.authorized.discount"
    _description = "POS Authorized Discounts"
    _rec_name = "code"

    code = fields.Char(required=True)
    discount_type = fields.Selection([
        ("percent", "Porcentaje"),
        ("amount", "Monto fijo"),
    ], required=True)

    value = fields.Float(required=True)
    expiration = fields.Datetime("Expira el")
    used = fields.Boolean(default=False)

    @api.model
    def validate_code(self, code_str):
        code = self.search([("code", "=", code_str.upper())], limit=1)
        if not code:
            return {"ok": False, "error": "Código incorrecto"}
        if code.used:
            return {"ok": False, "error": "Código ya utilizado"}
        if code.expiration and datetime.now() > code.expiration:
            return {"ok": False, "error": "Código expirado"}

        code.used = True

        return {
            "ok": True,
            "type": code.discount_type,
            "value": code.value,
        }
