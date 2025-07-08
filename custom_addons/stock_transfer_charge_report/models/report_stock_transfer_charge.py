from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte Simple de Traspasos con Precio Unitario y Peso'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids)
        res_docs = []
        for picking in pickings:
            total_precio = 0.0
            total_peso = 0.0
            lines = []
            for ml in picking.move_line_ids_without_package:
                cantidad = ml.qty_done or ml.quantity or 0.0
                precio_unitario = ml.product_id.standard_price or 0.0
                subtotal = cantidad * precio_unitario
                # asumimos product.weight en kg
                peso = (ml.product_id.weight or 0.0) * cantidad
                total_precio += subtotal
                total_peso += peso
                lines.append({
                    'producto':         ml.product_id.display_name,
                    'cantidad':         cantidad,
                    'uom':              ml.product_uom_id.name,
                    'precio_unitario':  precio_unitario,
                    'subtotal':         subtotal,
                    'peso':             peso,
                })
            res_docs.append({
                'name':               picking.name,
                'location_id':        picking.location_id.display_name,
                'location_dest_id':   picking.location_dest_id.display_name,
                'state':              picking.state,
                'picking_type_code':  picking.picking_type_code,
                'lines':              lines,
                'total_precio':       total_precio,
                'total_peso':         total_peso,
            })
        return {
            'doc_ids':   docids,
            'doc_model': 'stock.picking',
            'docs':      res_docs,
        }
