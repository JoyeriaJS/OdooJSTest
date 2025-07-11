from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte Simple de Traspasos'
    _auto = False

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids or [])

        pricelist = self.env['product.pricelist'].search(
            [('name', '=', 'Interno (CLP)')], limit=1)
        precios_interno = {}
        # precarga de precios internos
        if pricelist:
            items = self.env['product.pricelist.item'].search([
                ('pricelist_id', '=', pricelist.id),
                ('applied_on',   '=', '1_product'),
            ])
            for item in items:
                for v in item.product_tmpl_id.product_variant_ids:
                    precios_interno[v.id] = item.fixed_price or 0.0

        docs = []
        for p in pickings:
            lines = []
            total_std = total_int = 0.0
            for ml in p.move_line_ids_without_package:
                qty       = ml.quantity_done or ml.product_uom_qty or 0.0
                std_u     = ml.product_id.standard_price or 0.0
                int_u     = precios_interno.get(ml.product_id.id, 0.0)
                sub_std   = qty * std_u
                sub_int   = qty * int_u
                total_std += sub_std
                total_int += sub_int
                lines.append({
                    'producto':      ml.product_id.display_name,
                    'cantidad':      qty,
                    'uom':           ml.product_uom_id.name,
                    'price_unit':    std_u,
                    'price_int':     int_u,
                    'subtotal_std':  sub_std,
                    'subtotal_int':  sub_int,
                })
            docs.append({
                'name':         p.name,
                'origin':       p.location_id.display_name,
                'destination':  p.location_dest_id.display_name,
                'state':        p.state,
                'type':         p.picking_type_code,
                'lines':        lines,
                'total_std':    total_std,
                'total_int':    total_int,
            })
        return {
            'doc_ids':   pickings.ids,
            'doc_model': 'stock.picking',
            'docs':      docs,
        }
