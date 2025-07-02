from odoo import models, api

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte General de Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Toma los pickings seleccionados (o todos, para prueba)
        pickings = self.env['stock.picking'].browse(docids) if docids else self.env['stock.picking'].search([])
        return {
            'doc_ids': pickings.ids,
            'doc_model': 'stock.picking',
            'docs': pickings,
        }
