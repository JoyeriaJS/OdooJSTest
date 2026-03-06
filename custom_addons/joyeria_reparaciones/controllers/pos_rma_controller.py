from odoo import http
from odoo.http import request


class PosRMAController(http.Controller):

    @http.route('/pos/buscar_rma', type='json', auth='user', methods=['POST'])
    def buscar_rma(self, **kwargs):

        rma = kwargs.get('rma')

        if not rma:
            return {"error": "No se recibió el RMA"}

        reparacion = request.env['joyeria.reparacion'].sudo().search([
            ('name', '=', rma)
        ], limit=1)

        if not reparacion:
            return {"error": "RMA no encontrado"}

        return {
            "success": True,
            "rma": reparacion.name,
            "abono": reparacion.abono or 0,
        }