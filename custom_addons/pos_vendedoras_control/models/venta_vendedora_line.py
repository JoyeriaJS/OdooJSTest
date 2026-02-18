from odoo import models, fields, api
from odoo.exceptions import ValidationError


class VentaVendedoraLine(models.Model):
    _name = 'venta.vendedora.line'
    _description = 'Detalle de Tickets del Cierre'

    cierre_id = fields.Many2one(
        'venta.vendedora',
        ondelete='cascade'
    )

    # 👇 AHORA ES CHAR
    pos_reference_input = fields.Char(string="Número Ticket", required=True)

    pos_order_id = fields.Many2one(
        'pos.order',
        string="Orden POS",
        readonly=True
    )

    efectivo = fields.Float(string="Efectivo", readonly=True)
    transferencia = fields.Float(string="Transferencia", readonly=True)
    tarjeta = fields.Float(string="Tarjeta", readonly=True)

    _sql_constraints = [
        ('unique_ticket',
         'unique(pos_reference_input)',
         'Este ticket ya fue agregado.')
    ]

    # 🔥 BUSCAR ORDEN AUTOMÁTICAMENTE
    @api.onchange('pos_reference_input')
    def _onchange_buscar_ticket(self):

        if not self.pos_reference_input:
            return

        order = self.env['pos.order'].search([
            ('pos_reference', '=', self.pos_reference_input)
        ], limit=1)

        if not order:
            raise ValidationError("No existe una orden POS con ese número.")

        self.pos_order_id = order.id

        efectivo = 0.0
        transferencia = 0.0
        tarjeta = 0.0

        for payment in order.payment_ids:

            metodo = payment.payment_method_id.name.lower()

            # Clasificación más flexible
            if 'efectivo' in metodo:
                efectivo += payment.amount

            elif 'transfer' in metodo:
                transferencia += payment.amount

            elif 'tarjeta' in metodo or 'credito' in metodo or 'debito' in metodo:
                tarjeta += payment.amount

            else:
                # Si no coincide, lo mandamos a tarjeta por seguridad
                tarjeta += payment.amount

        self.efectivo = efectivo
        self.transferencia = transferencia
        self.tarjeta = tarjeta

