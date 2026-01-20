from odoo import models, fields, api
import random
import string
from datetime import datetime, timedelta
import pytz


class ReparacionAuthCode(models.Model):
    _name = "joyeria.reparacion.authcode"
    _description = "Códigos de autorización para reparaciones sin costo"
    _rec_name = "codigo"

    codigo = fields.Char(string="Código", readonly=True)
    used = fields.Boolean(string="Usado", default=False)
    fecha_generado = fields.Datetime(string="Fecha generado", default=fields.Datetime.now)

    # ⚠️ EL CAMPO fecha_creacion SE DEFINE UNA SOLA VEZ
    fecha_creacion = fields.Datetime(
        string="Fecha creación",
        default=lambda self: fields.Datetime.now(),
        readonly=True
    )

    usado_por_id = fields.Many2one("res.users", string="Usado por", readonly=True)
    fecha_uso = fields.Datetime("Fecha de uso", readonly=True)

    tiempo_restante = fields.Char(
        string="Tiempo restante",
        compute="_compute_tiempo_restante"
    )

    expired = fields.Boolean(
        string="Expirado",
        compute="_compute_expired",
        store=True
    )

    # --------------------------------------------
    # Generar código
    # --------------------------------------------
    def generar_codigo(self):
        """Generar código aleatorio de 6 caracteres"""
        self.codigo = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

    # --------------------------------------------
    # Tiempo restante
    # --------------------------------------------
    @api.depends("fecha_creacion", "expired")
    def _compute_tiempo_restante(self):
        for rec in self:

            if rec.expired:
                rec.tiempo_restante = "⛔ Código expirado"
                continue

            if not rec.fecha_creacion:
                rec.tiempo_restante = "No disponible"
                continue

            fecha_ini = rec.fecha_creacion

            # Normalizar a aware (UTC)
            if fecha_ini.tzinfo is None:
                fecha_ini = pytz.UTC.localize(fecha_ini)

            ahora = datetime.now(pytz.UTC)
            expira = fecha_ini + timedelta(hours=1)

            diff = expira - ahora

            if diff.total_seconds() <= 0:
                rec.tiempo_restante = "⛔ Código expirado"
            else:
                minutos = int(diff.total_seconds() // 60)
                segundos = int(diff.total_seconds() % 60)
                rec.tiempo_restante = f"⏳ {minutos} min {segundos} seg"

    # --------------------------------------------
    # Expiración automática
    # --------------------------------------------
    @api.depends("fecha_creacion", "used")
    def _compute_expired(self):
        for code in self:

            # Si ya está usado → expirado
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
                # 🔥 Expirar DEFINITIVAMENTE → lo marca como USADO también
                code.write({
                    "used": True,
                    "expired": True,
                    "fecha_uso": datetime.now(),
                    "usado_por_id": False
                })
                code.expired = True
            else:
                code.expired = False

    # --------------------------------------------
    # Crear código
    # --------------------------------------------
    @api.model
    def create(self, vals):
        rec = super().create(vals)
        codigo = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        rec.write({"codigo": codigo})
        return rec
