from odoo import models, fields, api
from odoo.exceptions import ValidationError
import random
import string
import logging
from datetime import datetime, timedelta
import pytz

class ReparacionAuthCode(models.Model):
    _name = "joyeria.reparacion.authcode"
    _description = "Códigos de autorización para reparaciones sin costo"
    _rec_name = "codigo"

    # ---------------------------------------------------------
    # CAMPOS
    # ---------------------------------------------------------
    codigo = fields.Char(string="Código", readonly=True)
    used = fields.Boolean(string="Usado", default=False)

    fecha_creacion = fields.Datetime(
        string="Fecha de creación",
        default=lambda self: fields.Datetime.now(),
        readonly=True
    )

    usado_por_id = fields.Many2one("res.users", string="Usado por", readonly=True)
    fecha_uso = fields.Datetime(string="Fecha de uso", readonly=True)

    expired = fields.Boolean(
        string="Expirado",
        compute="_compute_expired",
        store=True
    )

    tiempo_restante = fields.Char(
        string="Tiempo restante",
        compute="_compute_tiempo_restante"
    )

    # ---------------------------------------------------------
    # GENERAR CÓDIGO
    # ---------------------------------------------------------
    def generar_codigo(self):
        self.codigo = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

    # ---------------------------------------------------------
    # TIEMPO RESTANTE
    # ---------------------------------------------------------
    @api.depends("fecha_creacion", "expired")
    def _compute_tiempo_restante(self):
        for rec in self:

            if rec.expired:
                rec.tiempo_restante = "⛔ Expirado"
                continue

            if not rec.fecha_creacion:
                rec.tiempo_restante = "No disponible"
                continue

            fecha_ini = rec.fecha_creacion

            # Aseguramos aware
            if fecha_ini.tzinfo is None:
                fecha_ini = pytz.UTC.localize(fecha_ini)

            ahora = datetime.now(pytz.UTC)
            expira = fecha_ini + timedelta(hours=1)

            diff = expira - ahora

            if diff.total_seconds() <= 0:
                rec.tiempo_restante = "⛔ Expirado"
            else:
                minutos = int(diff.total_seconds() // 60)
                segundos = int(diff.total_seconds() % 60)
                rec.tiempo_restante = f"⏳ {minutos} min {segundos} seg"

    # ---------------------------------------------------------
    # CÁLCULO DE EXPIRACIÓN REAL
    # ---------------------------------------------------------
    @api.depends("fecha_creacion", "used")
    def _compute_expired(self):
        for code in self:

            if code.used:
                code.expired = True
                continue

            if not code.fecha_creacion:
                code.expired = False
                continue

            fecha_ini = code.fecha_creacion

            if fecha_ini.tzinfo is None:
                fecha_ini = pytz.UTC.localize(fecha_ini)

            ahora = datetime.now(pytz.UTC)
            expira = fecha_ini + timedelta(hours=1)

            if ahora >= expira:
                # Expirar automáticamente
                code.write({
                    'used': True,
                    'expired': True,
                    'fecha_uso': datetime.now(),
                    'usado_por_id': False,
                })
                code.expired = True
            else:
                code.expired = False

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------
    @api.model
    def create(self, vals):
        rec = super().create(vals)
        codigo = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        rec.write({"codigo": codigo})
        return rec
