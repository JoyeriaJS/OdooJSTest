from odoo import models

class RecommendationEngine(models.Model):
    _name = 'ai.recommendation.engine'
    _description = 'Recommendation Engine'

    def generate(self, sales_data, vendor_data, stock_data):

        message = "📊 ANÁLISIS SEMANAL\n\n"

        message += f"Órdenes última semana: {sales_data.get('orders_count_last_week')}\n"
        message += f"Órdenes semana anterior: {sales_data.get('orders_count_prev_week')}\n"
        message += f"Total última semana: {sales_data.get('total_last_week')}\n"
        message += f"Total semana anterior: {sales_data.get('total_prev_week')}\n\n"

        variation = sales_data.get('variation', 0)

        if variation < -10:
            message += f"⚠ Ventas bajaron {abs(round(variation,2))}%\n"
        elif variation > 10:
            message += f"📈 Ventas aumentaron {round(variation,2)}%\n"
        else:
            message += "Ventas estables.\n"

        if not sales_data.get('orders_count_last_week'):
            message += "\n⚠ No hay ventas registradas en los últimos 7 días.\n"

        return message
