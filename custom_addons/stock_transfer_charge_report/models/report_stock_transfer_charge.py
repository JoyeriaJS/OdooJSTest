from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte Simple de Traspasos con Precio Interno'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids) if docids else self.env['stock.picking'].search([])

        # Busca la lista de precios "Interno (CLP)"
        pricelist = self.env['product.pricelist'].search([('name', '=', 'Interno (CLP)')], limit=1)

        movimientos = []
        for picking in pickings:
            for ml in picking.move_line_ids_without_package:
                precio_interno = 0.0
                # Busca por variante primero
                if pricelist:
                    item = self.env['product.pricelist.item'].search([
                        ('pricelist_id', '=', pricelist.id),
                        ('product_id', '=', ml.product_id.id),  # buscar por variante
                    ], limit=1)
                    # Si no lo encuentra, busca por plantilla
                    if not item:
                        item = self.env['product.pricelist.item'].search([
                            ('pricelist_id', '=', pricelist.id),
                            ('product_tmpl_id', '=', ml.product_id.product_tmpl_id.id),
                        ], limit=1)
                    if item:
                        precio_interno = item.fixed_price

                movimientos.append({
                    'producto': ml.product_id.display_name or '',
                    'cantidad': ml.quantity or 0.0,
                    'uom': ml.product_uom_id.name or '',
                    'precio_interno': precio_interno,
                    'subtotal': (ml.quantity or 0.0) * precio_interno,
                    'origen': picking.location_id.display_name or '',
                    'destino': picking.location_dest_id.display_name or '',
                    'picking_name': picking.name or '',
                    'fecha': picking.date_done.strftime('%d/%m/%Y %H:%M:%S') if picking.date_done else '',
                    'estado': picking.state or '',
                    'tipo': picking.picking_type_code or '',
                })

        return {
            'docs': pickings,
            'movimientos': movimientos,
        }
