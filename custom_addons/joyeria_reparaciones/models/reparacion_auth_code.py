from odoo import models, fields, api
from odoo.exceptions import ValidationError
import random
import string
import logging
from datetime import datetime, timedelta
import pytz
from  pytz import utc
from pytz import timezone

class ReparacionAuthCode(models.Model):
    _name = "joyeria.reparacion.authcode"
    _description = "Códigos de autorización para reparaciones sin costo"
    _rec_name = "codigo"

    codigo = fields.Char(string="Código", readonly=True)
    used = fields.Boolean(string="Usado", default=False)
    fecha_generado = fields.Datetime(string="Fecha generado", default=fields.Datetime.now)
    #tienda_id = fields.Many2one("joyeria.tienda", string="Tienda", help="Opcional")
    # 🔥 CAMPOS NECESARIOS PARA REGISTRAR QUIÉN Y CUÁNDO SE USA EL CÓDIGO
    usado_por_id = fields.Many2one("res.users", string="Usado por", readonly=True)
    fecha_uso = fields.Datetime("Fecha de uso", readonly=True)
    fecha_creacion = fields.Datetime(string="Fecha creación", default=lambda self: fields.Datetime.now())
    tiempo_restante = fields.Char(string="Tiempo restante", compute="_compute_tiempo_restante")
    expirado = fields.Boolean(string="Expirado", compute="_compute_expirado", store=True)
    fecha_creacion = fields.Datetime(
    string="Fecha de creación",
    default=lambda self: fields.Datetime.now(),
    readonly=True
    )

    expired = fields.Boolean(
        string="Expirado",
        default=False,
        readonly=True
    )



    def generar_codigo(self):
        """Generar código aleatorio de 6 caracteres"""
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.codigo = code
    
    @api.depends("fecha_creacion")
    def _compute_tiempo_restante(self):
        for rec in self:
            if not rec.fecha_creacion:
                rec.tiempo_restante = "No disponible"
                continue

            # Convertir fecha_creacion siempre a aware (UTC)
            if rec.fecha_creacion.tzinfo is None:
                fecha_creacion_aware = pytz.UTC.localize(rec.fecha_creacion)
            else:
                fecha_creacion_aware = rec.fecha_creacion

            # Ahora actual en aware (UTC)
            ahora = datetime.now(pytz.UTC)

            # Expira 1 hora después
            expira = fecha_creacion_aware + timedelta(hours=1)

            diff = expira - ahora

            if diff.total_seconds() <= 0:
                rec.tiempo_restante = "⛔ Código expirado"
            else:
                minutos = int(diff.total_seconds() // 60)
                segundos = int(diff.total_seconds() % 60)
                rec.tiempo_restante = f"⏳ {minutos} min {segundos} seg"


    @api.depends("fecha_generado", "used")
    def _compute_expirado(self):
        """Marca automáticamente un código como expirado si ya pasó 1 hora."""
        for code in self:
            # Si ya está usado, automáticamente es expirado
            if code.used or not code.fecha_generado:
                code.expirado = True if code.used else False
                continue

            # Convertir fecha_generado a aware
            if code.fecha_generado.tzinfo is None:
                fecha_ini = pytz.UTC.localize(code.fecha_generado)
            else:
                fecha_ini = code.fecha_generado

            ahora = datetime.now(pytz.UTC)
            expira = fecha_ini + timedelta(hours=1)

            if ahora >= expira:
                # Expiró → marcar como usado automáticamente
                code.write({
                    'used': True,
                    'usado_por_id': False,
                    'fecha_uso': datetime.now(),
                })
                code.expirado = True
            else:
                code.expirado = False


    @api.model
    def create(self, vals):
        rec = super().create(vals)
        # Generar código
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        # Guardarlo en DB de verdad
        rec.write({"codigo": code})
        return rec
