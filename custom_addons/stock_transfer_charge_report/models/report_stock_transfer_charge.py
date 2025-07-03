from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte Simple de Traspasos con Precio Interno'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids) if docids else self.env['stock.picking'].search([])

        # Busca la lista de precios "Interno (CLP)" con ILIKE por si tiene espacios
        pricelist = self.env['product.pricelist'].search([('name', 'ilike', 'Interno (CLP)')], limit=1)

        # Pre-carga los precios internos para todos los productos involucrados
        precios_interno = {}
        if pricelist:
            items = self.env['product.pricelist.item'].search([
                ('pricelist_id', '=', pricelist.id),
                ('applied_on', '=', '1_product'),
            ])
            for item in items:
                # OJO: product_id, no product_tmpl_id (en muchos Odoo, product_id es el correcto para la regla)
                if item.product_id:
                    precios_interno[item.product_id.id] = item.fixed_price
                elif item.product_tmpl_id:
                    # fallback por si hay reglas por template
                    for prod in self.env['product.product'].search([('product_tmpl_id','=',item.product_tmpl_id.id)]):
                        precios_interno[prod.id] = item.fixed_price

        movimientos = []
        for picking in pickings:
            for ml in picking.move_line_ids_without_package:
                precio_interno = precios_interno.get(ml.product_id.id, 0.0)
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
