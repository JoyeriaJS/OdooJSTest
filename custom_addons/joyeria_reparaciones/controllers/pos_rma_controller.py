from odoo import http
from odoo.http import request


class PosRMAController(http.Controller):

    @http.route('/pos/buscar_rma', type='json', auth='user')
    def buscar_rma(self, rma):

        if not rma:
            return {
                'error': 'Debe ingresar un número de RMA.'
            }

        # buscar exactamente por la referencia de reparación
        reparacion = request.env['joyeria.reparacion'].sudo().search([
            ('name', '=', rma)
        ], limit=1)

        if not reparacion:
            return {
                'error': 'RMA no encontrado'
            }

        if not reparacion.abono or reparacion.abono <= 0:
            return {
                'error': 'RMA sin abono'
            }

        return {
            'abono': reparacion.abono
        }