from odoo import http
from odoo.http import request


class PosRMAController(http.Controller):

    @http.route('/pos/buscar_rma', type='json', auth='user')
    def buscar_rma(self, rma=None):

        if not rma:
            return {
                "success": False,
                "message": "Debe ingresar un RMA."
            }

        rma = str(rma).strip().upper()

        Reparacion = request.env['joyeria.reparacion'].sudo()

        # Buscar directamente
        reparacion = Reparacion.search([
            ('name', '=', rma)
        ], limit=1)

        # Si no existe, intentar con formato RMA/
        if not reparacion and not rma.startswith("RMA/"):

            numero = rma.zfill(5)
            codigo = f"RMA/{numero}"

            reparacion = Reparacion.search([
                ('name', '=', codigo)
            ], limit=1)

        # Si aún no existe
        if not reparacion:
            return {
                "success": False,
                "message": "El RMA no existe."
            }

        # Validar abono
        if not reparacion.abono or reparacion.abono <= 0:
            return {
                "success": False,
                "message": "El RMA no tiene valor de abono."
            }

        return {
            "success": True,
            "rma": reparacion.name,
            "abono": reparacion.abono,
            "cliente": reparacion.cliente_id.name if reparacion.cliente_id else "",
        }