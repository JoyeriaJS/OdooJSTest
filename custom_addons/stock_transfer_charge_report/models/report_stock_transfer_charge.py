from odoo import models, api
from collections import defaultdict

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte Simple de Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids) if docids else self.env['stock.picking'].search([])
        
        pricelist = self.env['product.pricelist'].search([('name', 'ilike', 'Interno')], limit=1)
        traspasos_por_mes = defaultdict(list)

        for picking in pickings:
            mes = picking.date_done.strftime('%B %Y') if picking.date_done else 'Sin Fecha'
            for ml in picking.move_line_ids_without_package:
                precio_interno = 0.0
                if pricelist:
                    item = self.env['product.pricelist.item'].search([
                        ('pricelist_id', '=', pricelist.id),
                        ('product_tmpl_id', '=', ml.product_id.product_tmpl_id.id),
                        ('applied_on', '=', '1_product'),
                    ], limit=1)
                    if item:
                        precio_interno = item.fixed_price
                subtotal = ml.quantity * precio_interno
                traspasos_por_mes[mes].append({
                    'code': ml.product_id.default_code or '',
                    'name': ml.product_id.display_name or '',
                    'qty': ml.quantity or 0.0,
                    'uom': ml.product_uom_id.name or '',
                    'origen': picking.location_id.display_name or '',
                    'destino': picking.location_dest_id.display_name or '',
                    'picking_name': picking.name or '',
                    'fecha': picking.date_done.strftime('%d/%m/%Y %H:%M:%S') if picking.date_done else '',
                    'estado': picking.state or '',
                    'precio_interno': precio_interno,
                    'subtotal_interno': subtotal,
                })

        # DEBUG: Esto imprime en el log de Odoo
        # print("DEBUG traspasos_por_mes", traspasos_por_mes)

        return {
            'traspasos_por_mes': traspasos_por_mes,
        }
