from odoo import http
from odoo.http import request


class PosRMAController(http.Controller):

    @http.route('/pos/buscar_rma', type='json', auth='user')
    def buscar_rma(self, **kwargs):

        numero_rma = kwargs.get("numero_rma")

        if not numero_rma:
            return {
                "error": "Debe ingresar un número de RMA"
            }

        numero_rma = numero_rma.strip().upper()

        # permitir escribir solo número (1162)
        if not numero_rma.startswith("RMA/"):
            numero_rma = f"RMA/{numero_rma.zfill(5)}"

        reparacion = request.env['joyeria.reparacion'].sudo().search([
            ('name', '=', numero_rma)
        ], limit=1)

        # RMA no existe
        if not reparacion:
            return {
                "error": f"El RMA {numero_rma} no existe"
            }

        # RMA sin abono
        if not reparacion.abono or reparacion.abono <= 0:
            return {
                "error": f"El RMA {numero_rma} no tiene abono registrado"
            }

        return {
            "success": True,
            "precio": reparacion.abono,
            "rma": reparacion.name
        }