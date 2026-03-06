from odoo import http
from odoo.http import request


class PosRMAController(http.Controller):

    @http.route('/pos/buscar_rma', type='json', auth='user')
    def buscar_rma(self, rma=None):

        if not rma:
            return {
                "error": "Debe ingresar un RMA."
            }

        rma = str(rma).strip().upper()

        # Permitir buscar sin escribir RMA/
        if not rma.startswith("RMA/"):
            rma = "RMA/" + rma.zfill(5)

        reparacion = request.env['joyeria.reparacion'].sudo().search([
            ('name', '=', rma)
        ], limit=1)

        # ❌ RMA NO EXISTE
        if not reparacion:
            return {
                "error": "not_found"
            }

        # ❌ RMA SIN ABONO
        if not reparacion.abono or reparacion.abono <= 0:
            return {
                "error": "no_abono"
            }

        # ✅ TODO OK
        return {
            "success": True,
            "rma": reparacion.name,
            "abono": reparacion.abono,
            "cliente": reparacion.cliente_id.name if reparacion.cliente_id else "",
        }