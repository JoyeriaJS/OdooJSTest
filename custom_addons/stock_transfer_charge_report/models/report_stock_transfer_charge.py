from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de Traspasos con Precio y Peso'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids)
        docs = []
        for picking in pickings:
            total_precio = 0.0
            total_peso = 0.0
            lines = []
            # iteramos cada línea de movimiento sin paquete
            for ml in picking.move_line_ids_without_package:
                cantidad = ml.qty_done or ml.quantity or 0.0
                precio_unitario = ml.product_id.standard_price or 0.0
                subtotal = cantidad * precio_unitario
                # usamos el campo `weight` del producto (en kg)
                peso_unitario = ml.product_id.weight or 0.0
                peso_linea = peso_unitario * cantidad

                total_precio += subtotal
                total_peso   += peso_linea

                lines.append({
                    'producto':        ml.product_id.display_name,
                    'cantidad':        cantidad,
                    'uom':             ml.product_uom_id.name,
                    'precio_unitario': precio_unitario,
                    'subtotal':        subtotal,
                    'peso_linea':      peso_linea,
                })

            docs.append({
                'name':              picking.name,
                'origen':            picking.location_id.display_name,
                'destino':           picking.location_dest_id.display_name,
                'estado':            picking.state,
                'tipo':              picking.picking_type_code,
                'lines':             lines,
                'total_precio':      total_precio,
                'total_peso':        total_peso,
            })

        return {
            'doc_ids':   docids,
            'doc_model': 'stock.picking',
            'docs':      docs,
        }
