from odoo import models, fields, api
from datetime import datetime

class PosAuthorizedDiscount(models.Model):
    _name = "pos.authorized.discount"
    _description = "Authorized POS Discount Codes"
    _rec_name = "code"

    code = fields.Char("Código", required=True, copy=False)
    discount_type = fields.Selection(
        [("percent", "Porcentaje"), ("amount", "Monto fijo")],
        required=True
    )
    value = fields.Float("Valor del descuento", required=True)

    expiration = fields.Datetime("Expira el")
    used = fields.Boolean("Usado", default=False)

    @api.model
    def generate_code(self):
        """Genera un código aleatorio tipo ABC12"""
        import random, string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    @api.model
    def validate_code(self, code_str):
        """Validación desde POS vía RPC."""
        code = self.search([("code", "=", code_str.upper())], limit=1)
        if not code:
            return {"ok": False, "error": "Código inexistente"}

        if code.used:
            return {"ok": False, "error": "Código ya fue utilizado"}

        if code.expiration and datetime.now() > code.expiration:
            return {"ok": False, "error": "El código expiró"}

        # Marcar como usado
        code.used = True

        return {
            "ok": True,
            "type": code.discount_type,
            "value": code.value,
        }
