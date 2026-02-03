from odoo import models, fields, api
from datetime import datetime, timedelta
import random
import string


class POSDiscountAuthCode(models.Model):
    _name = "pos.discount.authcode"
    _description = "Códigos para autorización de descuentos"

    codigo = fields.Char(string="Código", readonly=True)
    used = fields.Boolean("Usado", default=False)
    fecha_creacion = fields.Datetime(default=lambda self: fields.Datetime.now())
    fecha_uso = fields.Datetime()
    usuario_id = fields.Many2one("res.users")

    def create(self, vals):
        rec = super().create(vals)
        rec.codigo = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return rec

    def validar_codigo(self, codigo, user_id):
        code = self.search([("codigo", "=", codigo), ("used", "=", False)], limit=1)
        if not code:
            return False

        # Expira en 1 hora
        if datetime.now() > code.fecha_creacion + timedelta(hours=1):
            code.used = True
            return False

        # Marcar como usado
        code.write({
            "used": True,
            "fecha_uso": datetime.now(),
            "usuario_id": user_id
        })
        return True
