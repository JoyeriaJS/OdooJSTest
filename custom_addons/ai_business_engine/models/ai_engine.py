from odoo import models, fields

class AIBusinessEngine(models.Model):
    _name = 'ai.business.engine'
    _description = 'AI Business Decision Engine'

    analysis_result = fields.Text()

    def run_full_analysis(self):

        sales_data = self.env['ai.sales.analyzer'].analyze()

        total_last = sales_data.get('total_last_week', 0)
        total_prev = sales_data.get('total_prev_week', 0)
        variation = sales_data.get('variation', 0)

        message = f"""
    ANÁLISIS IA - POS

    Ventas última semana: ${round(total_last, 2)}
    Ventas semana anterior: ${round(total_prev, 2)}
    Variación: {variation}%

    """

        if variation > 10:
            message += "\n📈 Tendencia positiva fuerte. Considera aumentar inventario."
        elif variation < -10:
            message += "\n📉 Caída significativa. Revisar promociones o productos."
        else:
            message += "\n📊 Estabilidad en ventas."

        self.write({
            'analysis_result': message
        })

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }