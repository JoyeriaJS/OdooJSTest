
from odoo import models, fields, api
from datetime import datetime, timedelta
import random, string
import pytz

class PosDiscountCode(models.Model):
    _name = "pos.discount.code"
    _description = "Códigos de descuento autorizados para POS"
    _rec_name = "code"

    code = fields.Char("Código", readonly=True)
    discount_type = fields.Selection([
        ("percent", "Porcentaje"),
        ("fixed", "Monto fijo")
    ], string="Tipo de Descuento", default="percent", required=True)

    discount_value = fields.Float("Valor del Descuento", required=True)
    used = fields.Boolean("Usado", default=False, readonly=True)
    expired = fields.Boolean("Expirado", compute="_compute_expired", store=True)
    fecha_creacion = fields.Datetime(default=lambda self: fields.Datetime.now(), readonly=True)
    fecha_uso = fields.Datetime(readonly=True)
    usado_por = fields.Many2one("res.users", readonly=True)

    def generate_code(self):
        self.code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

    @api.depends("fecha_creacion", "used")
    def _compute_expired(self):
        for rec in self:
            if rec.used:
                rec.expired = True
                continue
            if not rec.fecha_creacion:
                rec.expired = False
                continue
            fecha = rec.fecha_creacion
            if fecha.tzinfo is None:
                fecha = pytz.UTC.localize(fecha)
            now = datetime.now(pytz.UTC)
            expira = fecha + timedelta(hours=1)
            if now >= expira:
                rec.expired = True
                rec.used = True
                rec.fecha_uso = datetime.now()
            else:
                rec.expired = False

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        rec.code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return rec

    def action_generate(self):
        for r in self:
            r.generate_code()
