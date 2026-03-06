from odoo import http
from odoo.http import request


class PosRMAController(http.Controller):

    @http.route('/pos/buscar_rma', type='json', auth='user')
    def buscar_rma(self, numero_rma):

        if not numero_rma:
            return {"error": "Debe ingresar un número de RMA"}

        numero_rma = numero_rma.strip().upper()

        # Permitir buscar solo el número (1162)
        if not numero_rma.startswith("RMA/"):
            numero_rma = f"RMA/{numero_rma.zfill(5)}"

        reparacion = request.env['joyeria.reparacion'].sudo().search([
            ('name', '=', numero_rma)
        ], limit=1)

        if not reparacion:
            return {"error": "El RMA no existe"}

        if not reparacion.abono or reparacion.abono <= 0:
            return {"error": "Este RMA no tiene saldo de abono"}

        return {
            "precio": reparacion.abono,
            "rma": reparacion.name
        }