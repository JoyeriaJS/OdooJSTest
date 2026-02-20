from odoo import models, fields, api

class AIBusinessEngine(models.Model):
    _name = 'ai.business.engine'
    _description = 'AI Business Decision Engine'

    name = fields.Char(default="Análisis Inteligente")
    analysis_result = fields.Text()

    @api.model
    def action_open_dashboard(self):
        record = self.search([], limit=1)
        if not record:
            record = self.create({})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ai.business.engine',
            'view_mode': 'form',
            'res_id': record.id,
            'target': 'current',
        }

    def run_full_analysis(self):

        sales_data = self.env['ai.sales.analyzer'].analyze()
        vendor_data = self.env['ai.vendor.analyzer'].analyze()
        stock_data = self.env['ai.stock.predictor'].analyze()

        recommendation = self.env['ai.recommendation.engine'].generate(
            sales_data,
            vendor_data,
            stock_data
        )

        self.sudo().write({
            'analysis_result': recommendation or "No se generó análisis."
        })

        return {'type': 'ir.actions.client', 'tag': 'reload'}