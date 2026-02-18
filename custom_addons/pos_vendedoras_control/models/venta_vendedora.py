from odoo import models, fields, api
from odoo.exceptions import ValidationError


class VentaVendedora(models.Model):
    _name = 'venta.vendedora'
    _description = 'Control Diario de Ventas por Vendedora'

    _sql_constraints = [
        ('unique_pos_order', 'unique(pos_order_id)',
         'Esta orden POS ya fue registrada.')
    ]

    # ---------------------------------------------------------
    # CAMPOS PRINCIPALES
    # ---------------------------------------------------------

    name = fields.Char(string="Referencia", default="Nuevo", copy=False)

    user_id = fields.Many2one(
        'res.users',
        string="Vendedora",
        required=True,
        default=lambda self: self.env.user
    )

    fecha = fields.Date(
        string="Fecha",
        default=fields.Date.today
    )

    pos_order_id = fields.Many2one(
        'pos.order',
        string="Orden POS"
    )

    pos_reference_input = fields.Char(
        string="Escanear QR / Número Ticket"
    )

    # ---------------------------------------------------------
    # MONTOS POR MÉTODO DE PAGO
    # ---------------------------------------------------------

    efectivo = fields.Float(string="Venta Efectivo", readonly=True)
    transferencia = fields.Float(string="Venta Transferencia", readonly=True)
    tarjeta = fields.Float(string="Venta Tarjeta Crédito", readonly=True)

    total_ventas = fields.Float(
        string="Total Ventas",
        compute="_compute_totales",
        store=True
    )

    gastos = fields.Float(
        string="Gastos / Depósito Efectivo"
    )

    venta_neta = fields.Float(
        string="Venta Neta",
        compute="_compute_totales",
        store=True
    )

    # ---------------------------------------------------------
    # SECUENCIA AUTOMÁTICA
    # ---------------------------------------------------------

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('venta.vendedora') or 'Nuevo'
        return super(VentaVendedora, self).create(vals)

    # ---------------------------------------------------------
    # CAPTURA AUTOMÁTICA DE ORDEN POS
    # ---------------------------------------------------------

    @api.onchange('pos_reference_input')
    def _onchange_buscar_orden(self):

        if not self.pos_reference_input:
            return

        order = self.env['pos.order'].search([
            ('pos_reference', '=', self.pos_reference_input.strip())
        ], limit=1)

        if not order:
            return {
                'warning': {
                    'title': 'Orden no encontrada',
                    'message': 'No se encontró la orden POS ingresada.'
                }
            }

        self.pos_order_id = order.id

        efectivo = 0.0
        transferencia = 0.0
        tarjeta = 0.0

        for payment in order.payment_ids:
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

        # Limpia el campo para escanear otro
        self.pos_reference_input = False

    # ---------------------------------------------------------
    # CÁLCULOS
    # ---------------------------------------------------------

    @api.depends('efectivo', 'transferencia', 'tarjeta', 'gastos')
    def _compute_totales(self):
        for rec in self:
            rec.total_ventas = rec.efectivo + rec.transferencia + rec.tarjeta
            rec.venta_neta = rec.total_ventas - rec.gastos
