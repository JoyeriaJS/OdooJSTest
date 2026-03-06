from odoo import http
from odoo.http import request


class PosRMAController(http.Controller):

    @http.route('/pos/buscar_rma', type='json', auth='user')
    def buscar_rma(self):

        data = request.jsonrequest
        rma = data.get("rma")

        if not rma:
            return False

        reparacion = request.env['joyeria.reparacion'].sudo().search([
            ('name', '=', rma)
        ], limit=1)

        if not reparacion:
            return False

        if not reparacion.abono:
            return False

        return {
            "abono": reparacion.abono
        }