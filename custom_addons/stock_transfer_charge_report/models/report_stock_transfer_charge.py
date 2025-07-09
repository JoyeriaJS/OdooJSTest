from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge'        # ← nombre corto
    _description = 'Reporte Simple de Traspasos'
    _auto = False   

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) Cargar pickings
        pickings = self.env['stock.picking'].browse(docids) if docids else self.env['stock.picking'].search([])

        # 2) Cargar la pricelist “Interno (CLP)”
        pricelist = self.env['product.pricelist'].search([('name', '=', 'Interno (CLP)')], limit=1)

        movimientos = []
        total_interno = 0.0

        for picking in pickings:
            for ml in picking.move_line_ids_without_package:
                qty = ml.qty_done or ml.quantity or 0.0

                # 3) Buscar el precio interno para este producto
                if pricelist:
                    item = self.env['product.pricelist.item'].search([
                        ('pricelist_id', '=', pricelist.id),
                        ('product_tmpl_id', '=', ml.product_id.product_tmpl_id.id),
                        ('applied_on', '=', '1_product'),
                    ], limit=1)
                    precio_int = item.fixed_price if item else 0.0
                else:
                    precio_int = 0.0

                subtotal_int = qty * precio_int
                total_interno += subtotal_int

                movimientos.append({
                    'code':              ml.product_id.default_code or '',
                    'name':              ml.product_id.display_name or '',
                    'qty':               ml.quantity or 0.0,
                    'uom':               ml.product_uom_id.name or '',
                    'origen':            picking.location_id.display_name or '',
                    'destino':           picking.location_dest_id.display_name or '',
                    'picking_name':      picking.name or '',
                    'fecha':             (picking.date_done.strftime('%d/%m/%Y %H:%M:%S')
                                          if picking.date_done else ''),
                    'estado':            picking.state or '',
                    'precio_interno':    precio_int,
                    'subtotal_interno':  subtotal_int,
                })

        return {
            'movimientos':    movimientos,
            'total_interno':  total_interno,
            'pickings': pickings,
        }
