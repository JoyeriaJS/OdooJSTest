# report_stock_transfer_charge.py

from odoo import api, models

class StockTransferChargeReport(models.AbstractModel):
    _name = 'report.mi_modulo.stock_transfer_charge'
    _description = 'Reporte de cargos entre locales'

    @api.model
    def _get_report_values(self, docids, data=None):
        # 1) Cargamos y ordenamos los pickings por fecha de ejecución
        pickings = self.env['stock.picking'].browse(docids or []).sorted('date_done')

        # 2) Obtenemos la pricelist "Interno"
        pricelist = self.env['product.pricelist'].search(
            [('name', 'ilike', 'Interno (CLP) (CLP)')], limit=1)

        return {
            'doc_model': 'stock.picking',
            'doc_ids': pickings.ids,
            'docs': pickings,
            'pricelist': pricelist,
        }
