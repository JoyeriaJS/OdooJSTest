from odoo import models, fields

class AIBusinessEngine(models.Model):
    _name = 'ai.business.engine'
    _description = 'AI Business Decision Engine'

    name = fields.Char(default="Análisis Inteligente")
    analysis_result = fields.Text()

    def run_full_analysis(self):

        sales_data = self.env['ai.sales.analyzer'].analyze()
        vendor_data = self.env['ai.vendor.analyzer'].analyze()
        stock_data = self.env['ai.stock.predictor'].analyze()

        recommendation = self.env['ai.recommendation.engine'].generate(
            sales_data,
            vendor_data,
            stock_data
        )

        self.analysis_result = recommendation
