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

            ahora = datetime.now(pytz.UTC)
            expira = rec.fecha_creacion + timedelta(hours=1)

            diff = expira - ahora

            if diff.total_seconds() <= 0:
                rec.tiempo_restante = "⛔ Código expirado"
            else:
                minutos = int(diff.total_seconds() // 60)
                segundos = int(diff.total_seconds() % 60)
                rec.tiempo_restante = f"⏳ {minutos} min {segundos} seg"

    @api.model
    def _expirar_codigos(self):
        """Expira automáticamente códigos con más de 1 hora sin usar."""
        ahora = fields.Datetime.now()

        codigos = self.search([
            ('used', '=', False),
            ('expired', '=', False)
        ])

        for code in codigos:
            if code.fecha_creacion:
                limite = code.fecha_creacion + timedelta(hours=1)
                if ahora >= limite:
                    code.write({
                        'expired': True,
                        'used': True,
                        'fecha_uso': ahora,
                        'usado_por_id': None,  # No lo usó un usuario
                    })
                    _logger = logging.getLogger(__name__)
                    _logger.warning(f"⚠ Código expirado automáticamente: {code.codigo}")

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        # Generar código
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        # Guardarlo en DB de verdad
        rec.write({"codigo": code})
        return rec
