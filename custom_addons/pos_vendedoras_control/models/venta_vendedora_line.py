from odoo import models, fields, api
from odoo.exceptions import ValidationError


class VentaVendedoraLine(models.Model):
    _name = 'venta.vendedora.line'
    _description = 'Detalle de Tickets del Cierre'

    cierre_id = fields.Many2one(
        'venta.vendedora',
        ondelete='cascade'
    )

    pos_reference_input = fields.Char(
        string="Número Ticket",
        required=True
    )

    pos_order_id = fields.Many2one(
        'pos.order',
        string="Orden POS"
    )

    efectivo = fields.Float(string="Efectivo")
    transferencia = fields.Float(string="Transferencia")
    tarjeta = fields.Float(string="Tarjeta")

    _sql_constraints = [
        ('unique_ticket',
         'unique(pos_reference_input)',
         'Este ticket ya fue agregado.')
    ]

    # ==============================
    # FUNCIÓN CENTRAL DE CÁLCULO
    # ==============================
    def _calcular_pagos(self):

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

            if 'efectivo' in metodo:
                efectivo += payment.amount
            elif 'transfer' in metodo:
                transferencia += payment.amount
            elif 'tarjeta' in metodo or 'credito' in metodo or 'debito' in metodo:
                tarjeta += payment.amount
            else:
                tarjeta += payment.amount

        self.efectivo = efectivo
        self.transferencia = transferencia
        self.tarjeta = tarjeta

    # ==============================
    # ONCHANGE (solo visual)
    # ==============================
    @api.onchange('pos_reference_input')
    def _onchange_ticket(self):
        if self.pos_reference_input:
            self._calcular_pagos()

    # ==============================
    # CREATE (al guardar)
    # ==============================
    @api.model
    def create(self, vals):
        record = super().create(vals)
        record._calcular_pagos()
        return record

    # ==============================
    # WRITE (si editas)
    # ==============================
    def write(self, vals):
        res = super().write(vals)
        for record in self:
            if 'pos_reference_input' in vals:
                record._calcular_pagos()
        return res
