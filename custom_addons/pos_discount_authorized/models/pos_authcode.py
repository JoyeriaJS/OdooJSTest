from odoo import models, fields, api
from datetime import datetime, timedelta
import random
import string
import pytz


class PosDiscountAuthCode(models.Model):
    _name = "pos.discount.authcode"
    _description = "Códigos de autorización POS"
    _rec_name = "codigo"

    codigo = fields.Char("Código", readonly=True)
    usado = fields.Boolean("Usado", default=False)
    fecha_creacion = fields.Datetime("Creado en", default=lambda self: fields.Datetime.now())
    fecha_uso = fields.Datetime("Fecha de uso")
    usuario_id = fields.Many2one("res.users", string="Usado por")
    expirado = fields.Boolean("Expirado", compute="_compute_expired", store=True)

    @api.model
    def create(self, vals):
        vals["codigo"] = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return super().create(vals)

    @api.depends("fecha_creacion", "usado")
    def _compute_expired(self):
        for rec in self:
            if rec.usado:
                rec.expirado = True
                continue

            fecha_ini = rec.fecha_creacion.replace(tzinfo=pytz.UTC)
            expira = fecha_ini + timedelta(hours=1)
            ahora = datetime.now(pytz.UTC)

            rec.expirado = ahora >= expira

    # Validación RPC para el POS
    @api.model
    def validar_codigo(self, codigo, usuario_id):
        code = self.search([("codigo", "=", codigo)], limit=1)

        if not code:
            return False
        if code.usado:
            return False
        if code.expirado:
            return False

        code.write({
            "usado": True,
            "fecha_uso": fields.Datetime.now(),
            "usuario_id": usuario_id,
        })
        return True
