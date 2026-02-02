from odoo import models, fields, api
from datetime import datetime

class PosAuthorizedDiscount(models.Model):
    _name = "pos.authorized.discount"
    _description = "Códigos autorizados para descuento en POS"

    code = fields.Char(required=True)
    discount_type = fields.Selection([
        ("percent", "Porcentaje"),
        ("fixed", "Monto fijo"),
    ], required=True)

    value = fields.Float("Valor del descuento", required=True)
    expires_at = fields.Datetime("Expira el", required=True)
    used = fields.Boolean("Ya utilizado", default=False)

    def validate_code(self):
        """Validación llamada desde JS"""
        self.ensure_one()
        if self.used:
            return {"ok": False, "msg": "Código ya fue utilizado"}

        if self.expires_at < datetime.now():
            return {"ok": False, "msg": "Código expirado"}

        return {
            "ok": True,
            "type": self.discount_type,
            "value": self.value,
        }
