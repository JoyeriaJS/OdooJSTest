# models/report_stock_transfer_charge.py
from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'    # <-- esto
    _description = 'Reporte de cargos entre locales'
    _auto = False

    @api.model
    def _get_report_values(self, docids, data=None):
        pickings = self.env['stock.picking'].browse(docids or [])

        # 1) Buscamos la tarifa "Interno (CLP)"
        pricelist = self.env['product.pricelist'].search(
            [('name', '=', 'Interno (CLP)')], limit=1)

        # 2) Construimos el dict { variante_id: precio_interno }
        precios_interno = {}
        if pricelist:
            items = self.env['product.pricelist.item'].search([
                ('pricelist_id', '=', pricelist.id),
                ('applied_on',    '=', '1_product'),
            ])
            for item in items:
                for var in item.product_tmpl_id.product_variant_ids:
                    precios_interno[var.id] = item.fixed_price or 0.0

        return {
            'doc_ids':         pickings.ids,
            'doc_model':       'stock.picking',
            'docs':            pickings,
            'precios_interno': precios_interno,            # <-- esto
        }
