from odoo import models, fields, api
from odoo.exceptions import ValidationError
import random
import string

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

    def generar_codigo(self):
        """Generar código aleatorio de 6 caracteres"""
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.codigo = code

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        # Generar código
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        # Guardarlo en DB de verdad
        rec.write({"codigo": code})
        return rec
