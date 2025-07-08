from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de Traspasos con Peso y Firma'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids)
        docs = []

        for picking in pickings:
            total_peso = 0.0
            total_precio = 0.0
            lines = []

            for ml in picking.move_line_ids_without_package:
                producto = ml.product_id
                # en Odoo 17 el stock.move.line registra qty_done
                cantidad = ml.qty_done or 0.0
                precio_unitario = producto.standard_price or 0.0
                peso_unitario = producto.weight or 0.0  # en kg
                peso_trasladado = peso_unitario * cantidad
                subtotal = cantidad * precio_unitario

                total_peso += peso_trasladado
                total_precio += subtotal

                lines.append({
                    'producto': producto.display_name,
                    'cantidad': cantidad,
                    'uom': ml.product_uom_id.name,
                    'precio_unitario': precio_unitario,
                    'peso': peso_trasladado,
                    'subtotal': subtotal,
                })

            docs.append({
                'name':             picking.name,
                'location_id':      picking.location_id.display_name,
                'location_dest_id': picking.location_dest_id.display_name,
                'state':            picking.state,
                'picking_type_code': picking.picking_type_code,
                'total_peso':       total_peso,
                'total_precio':     total_precio,
                'lines':            lines,
            })

        return {
            'docs': docs,
        }
