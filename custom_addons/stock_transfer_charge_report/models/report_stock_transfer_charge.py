# models/report_stock_transfer_charge.py
from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte Simple de Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids) \
                   if docids else self.env['stock.picking'].search([])

        # 1) Busca la pricelist "Interno (CLP)"
        pricelist = self.env['product.pricelist'].search(
            [('name','=','Interno (CLP)')], limit=1)

        # 2) Construye el diccionario product_id → precio interno
        precios_interno = {}
        for prod in pickings.mapped('move_line_ids_without_package.product_id'):
            precios_interno[prod.id] = 0.0
            if pricelist:
                item = self.env['product.pricelist.item'].search([
                    ('pricelist_id','=',pricelist.id),
                    ('product_tmpl_id','=',prod.product_tmpl_id.id),
                    ('applied_on','=','1_product'),
                ], limit=1)
                precios_interno[prod.id] = item.fixed_price or 0.0

        return {
            'doc_ids':         docids,
            'doc_model':       'stock.picking',
            'docs':            pickings,
            # **Aquí**, metemos el mapa de precios al nivel raíz
            'precios_interno': precios_interno,
        }
