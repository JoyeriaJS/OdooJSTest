from odoo import models

class StockPredictor(models.Model):
    _name = 'ai.stock.predictor'
    _description = 'Stock Predictor'

    def analyze(self):

        products = self.env['product.product'].search([
            ('qty_available', '>=', 0)
        ])

        low_stock = []

        for product in products:
            if product.qty_available < 5:
                low_stock.append({
                    'product': product.name,
                    'qty': product.qty_available
                })

        return low_stock
