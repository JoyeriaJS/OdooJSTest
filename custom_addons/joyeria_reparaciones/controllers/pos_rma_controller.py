from odoo import http
from odoo.http import request


class PosRMAController(http.Controller):

    @http.route('/pos/buscar_rma', type='json', auth='user')
    def buscar_rma(self, rma):

        reparacion = request.env['joyeria.reparacion'].sudo().search([
            ('name', '=', rma)
        ], limit=1)

        if not reparacion:
            return {
                'error': 'RMA no encontrado'
            }

        if not reparacion.abono:
            return {
                'error': 'El RMA no tiene abono'
            }

        return {
            'precio': reparacion.abono,
            'rma': reparacion.name
        }