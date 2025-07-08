from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte Simple de Traspasos con Precio Interno'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids)
        res_docs = []
        for picking in pickings:
            total_precio = 0.0
            total_peso = 0.0
            lines = []
            for ml in picking.move_line_ids_without_package:
                qty     = ml.qty_done or ml.quantity or 0.0
                precio  = ml.product_id.standard_price or 0.0
                subtotal= qty * precio
                peso    = (ml.product_id.weight or 0.0) * qty
                total_precio += subtotal
                total_peso  += peso
                lines.append({
                    'producto':       ml.product_id.display_name,
                    'cantidad':       qty,
                    'uom':            ml.product_uom_id.name,
                    'precio_unitario': precio,
                    'peso':           peso,
                    'subtotal':       subtotal,
                })
            res_docs.append({
                'name':              picking.name,
                'location_id':       picking.location_id.display_name,
                'location_dest_id':  picking.location_dest_id.display_name,
                'state':             picking.state,
                'picking_type_code': picking.picking_type_code,
                'lines':             lines,
                'total_precio':      total_precio,
                'total_peso':        total_peso,
            })
        return {
            'doc_ids':   docids,
            'doc_model': 'stock.picking',
            'docs':      res_docs,
        }
