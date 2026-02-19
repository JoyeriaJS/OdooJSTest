from odoo import models

class RecommendationEngine(models.Model):
    _name = 'ai.recommendation.engine'
    _description = 'Recommendation Engine'

    def generate(self, sales_data, vendor_data, stock_data):

        message = ""

        # Ventas
        if sales_data['variation'] < -10:
            message += f"⚠ Ventas bajaron {abs(round(sales_data['variation'],2))}% esta semana.\n"
        elif sales_data['variation'] > 10:
            message += f"📈 Ventas aumentaron {round(sales_data['variation'],2)}% esta semana.\n"
        else:
            message += "Ventas estables.\n"

        # Vendedores
        if vendor_data:
            top_vendor = max(vendor_data, key=vendor_data.get)
            message += f"🏆 Mejor rendimiento: {top_vendor}\n"

        # Stock
        if stock_data:
            message += "\n⚠ Productos con bajo stock:\n"
            for product in stock_data:
                message += f"- {product['product']} (Stock: {product['qty']})\n"

        return message
