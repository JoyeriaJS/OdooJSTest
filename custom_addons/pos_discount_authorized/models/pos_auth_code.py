from odoo import models, fields, api
import random
from datetime import datetime, timedelta
import pytz


class PosDiscountAuthCode(models.Model):
    _name = "pos.discount.authcode"
    _description = "Códigos de autorización para descuentos POS"
    _rec_name = "codigo"

    codigo = fields.Char(string="Código", readonly=True)
    used = fields.Boolean(string="Usado", default=False)

    fecha_creacion = fields.Datetime(default=lambda self: fields.Datetime.now(), readonly=True)
    fecha_uso = fields.Datetime(readonly=True)

    usado_por_id = fields.Many2one("res.users", readonly=True)
    expired = fields.Boolean(string="Expirado", compute="_compute_expired", store=True)

    def generar_codigo(self):
        self.codigo = "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=6))

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        rec.generar_codigo()
        return rec

    @api.depends("fecha_creacion", "used")
    def _compute_expired(self):
        for rec in self:
            if rec.used:
                rec.expired = True
                continue
            expira = rec.fecha_creacion + timedelta(hours=1)
            rec.expired = datetime.now(pytz.UTC) > expira

    def validar_codigo(self, codigo, user_id):
        code = self.search([("codigo", "=", codigo)], limit=1)

        if not code or code.used or code.expired:
            return False

        code.write({
            "used": True,
            "fecha_uso": datetime.now(),
            "usado_por_id": user_id,
        })

        return True
