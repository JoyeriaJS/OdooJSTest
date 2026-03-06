from odoo import http
from odoo.http import request


class PosRMAController(http.Controller):

    @http.route('/pos/buscar_rma', type='json', auth='user', methods=['POST'])
    def buscar_rma(self):

        data = request.get_json_data()

        rma = data.get("rma")

        if not rma:
            return {
                "success": False,
                "message": "Debe ingresar un RMA"
            }

        reparacion = request.env['joyeria.reparacion'].sudo().search([
            ('name', '=', rma)
        ], limit=1)

        if not reparacion:
            return {
                "success": False,
                "message": "RMA no encontrado"
            }

        if not reparacion.abono:
            return {
                "success": False,
                "message": "El RMA no tiene valor de abono"
            }

        return {
            "success": True,
            "precio": reparacion.abono
        }