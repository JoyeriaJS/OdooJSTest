from odoo import models, fields, api
from odoo.exceptions import ValidationError


class VentaVendedoraLine(models.Model):
    _name = 'venta.vendedora.line'
    _description = 'Detalle de Tickets del Cierre'

    _sql_constraints = [
        ('unique_ticket', 'unique(pos_order_id)',
         'Este ticket ya fue registrado en otro cierre.')
    ]

    cierre_id = fields.Many2one(
        'venta.vendedora',
        string="Cierre",
        required=True,
        ondelete='cascade'
    )

    pos_order_id = fields.Many2one(
        'pos.order',
        string="Orden POS",
        domain="[('state','=','paid')]",
        required=True
    )

    pos_reference = fields.Char(
        related='pos_order_id.pos_reference',
        string="Número Ticket",
        store=True
    )

    efectivo = fields.Float(string="Efectivo")
    transferencia = fields.Float(string="Transferencia")
    tarjeta = fields.Float(string="Tarjeta")

    @api.onchange('pos_order_id')
    def _onchange_pos_order(self):
        if not self.pos_order_id:
            return

        efectivo = 0.0
        transferencia = 0.0
        tarjeta = 0.0

        for payment in self.pos_order_id.payment_ids:
            metodo = payment.payment_method_id.name.strip()

            if metodo == 'Venta Efectivo':
                efectivo += payment.amount
            elif metodo == 'Venta Transferencia':
                transferencia += payment.amount
            elif metodo == 'Venta Tarjeta Credito':
                tarjeta += payment.amount

        self.efectivo = efectivo
        self.transferencia = transferencia
        self.tarjeta = tarjeta
