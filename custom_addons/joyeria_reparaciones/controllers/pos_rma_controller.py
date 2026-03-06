from odoo import http
from odoo.http import request


class PosRMAController(http.Controller):

    @http.route('/pos/buscar_rma', type='json', auth='user', methods=['POST'], csrf=False)
    def buscar_rma(self, **kwargs):

        # Obtener rma desde JSON
        rma_input = kwargs.get('rma')

        if not rma_input:
            return {
                "success": False,
                "message": "Debe ingresar un número de RMA"
            }

        rma_input = str(rma_input).strip().upper()

        # Si escriben solo número (ej 1162)
        if not rma_input.startswith("RMA/"):
            try:
                numero = int(rma_input)
                rma_input = f"RMA/{numero:05d}"
            except:
                pass

        # Buscar reparación
        reparacion = request.env['joyeria.reparacion'].sudo().search([
            ('name', '=', rma_input)
        ], limit=1)

        if not reparacion:
            return {
                "success": False,
                "message": "RMA no encontrado"
            }

        if not reparacion.abono or reparacion.abono <= 0:
            return {
                "success": False,
                "message": "RMA sin abono"
            }

        return {
            "success": True,
            "precio": reparacion.abono,
            "rma": reparacion.name
        }