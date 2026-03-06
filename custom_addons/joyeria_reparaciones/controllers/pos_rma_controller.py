from odoo import http
from odoo.http import request


class PosRMAController(http.Controller):

    @http.route('/pos/buscar_rma', type='json', auth='user')
    def buscar_rma(self, **kwargs):

        rma = kwargs.get('rma')

        if not rma:
            return {"error": "RMA vacío"}

        reparacion = request.env['joyeria.reparacion'].sudo().search([
            ('referencia_reparacion', '=', rma)
        ], limit=1)

        if not reparacion:
            return {"error": "RMA no encontrado"}

        if not reparacion.abono:
            return {"error": "El RMA no tiene abono"}

        return {
            "abono": reparacion.abono,
            "referencia": reparacion.referencia_reparacion
        }
    