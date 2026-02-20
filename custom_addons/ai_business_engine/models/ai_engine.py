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

        recommendation = f"""
ANÁLISIS IA

Órdenes última semana: {sales_data.get('orders_count_last_week')}
Total última semana: {sales_data.get('total_last_week')}
Variación: {round(sales_data.get('variation', 0), 2)}%
"""

        self.sudo().write({
            'analysis_result': recommendation
        })

        return {'type': 'ir.actions.client', 'tag': 'reload'}