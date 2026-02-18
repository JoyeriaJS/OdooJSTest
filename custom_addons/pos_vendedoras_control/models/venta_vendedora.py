from odoo import models, fields, api
from odoo.exceptions import ValidationError


class VentaVendedora(models.Model):
    _name = 'venta.vendedora'
    _description = 'Cierre Diario de Ventas por Vendedora'
    _order = 'fecha desc'

    name = fields.Char(string="Referencia", default="Nuevo", copy=False)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('closed', 'Cerrado')
    ], default='draft')

    user_id = fields.Many2one(
        'res.users',
        string="Vendedora",
        required=True,
        default=lambda self: self.env.user
    )

    fecha = fields.Date(
        string="Fecha",
        default=fields.Date.today,
        required=True
    )

    gastos = fields.Float(string="Gastos / Depósito")

    line_ids = fields.One2many(
        'venta.vendedora.line',
        'cierre_id',
        string="Tickets"
    )

    total_efectivo = fields.Float(compute="_compute_totales", store=True)
    total_transferencia = fields.Float(compute="_compute_totales", store=True)
    total_tarjeta = fields.Float(compute="_compute_totales", store=True)
    total_ventas = fields.Float(compute="_compute_totales", store=True)
    venta_neta = fields.Float(compute="_compute_totales", store=True)

    # SECUENCIA
    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('venta.vendedora') or 'Nuevo'
        return super().create(vals)

    # CÁLCULOS
    @api.depends('line_ids.efectivo',
                 'line_ids.transferencia',
                 'line_ids.tarjeta',
                 'gastos')
    def _compute_totales(self):
        for rec in self:
            rec.total_efectivo = sum(rec.line_ids.mapped('efectivo'))
            rec.total_transferencia = sum(rec.line_ids.mapped('transferencia'))
            rec.total_tarjeta = sum(rec.line_ids.mapped('tarjeta'))

            rec.total_ventas = (
                rec.total_efectivo +
                rec.total_transferencia +
                rec.total_tarjeta
            )

            rec.venta_neta = rec.total_ventas - rec.gastos

    # BOTÓN CERRAR DÍA
    def action_cerrar_dia(self):
        for rec in self:
            if not rec.line_ids:
                raise ValidationError("No puede cerrar un día sin tickets.")
            rec.state = 'closed'
