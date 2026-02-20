from odoo import models, fields

class AIBusinessEngine(models.Model):
    _name = 'ai.business.engine'
    _description = 'AI Business Decision Engine'

    analysis_result = fields.Html()

    def run_full_analysis(self):

        analyzer = self.env['ai.sales.analyzer']
        sales_data = analyzer.analyze()

        total_last = sales_data.get('total_last_week', 0)
        total_prev = sales_data.get('total_prev_week', 0)
        variation = sales_data.get('variation', 0)

        orders_last_week = self.env['pos.order'].search([
            ('state', 'in', ['paid', 'done', 'invoiced'])
        ])

        orders_count = len(orders_last_week)
        avg_ticket = 0
        if orders_count:
            avg_ticket = total_last / orders_count

        # Determinar tendencia
        if variation > 10:
            trend_text = "📈 Crecimiento fuerte"
            decision = "Recomendación: aumentar inventario en productos de mayor rotación."
        elif variation < -10:
            trend_text = "📉 Disminución importante"
            decision = "Recomendación: activar promociones o revisar precios."
        else:
            trend_text = "📊 Estabilidad"
            decision = "Recomendación: mantener estrategia actual y monitorear."

        message = f"""
        <h1>🤖 AI Business Intelligence</h1>
        <hr/>

        <h2>📊 Indicadores Clave</h2>
        <ul>
            <li><strong>💰 Ventas Última Semana:</strong> ${round(total_last, 2)}</li>
            <li><strong>🧾 Órdenes:</strong> {orders_count}</li>
            <li><strong>🎯 Ticket Promedio:</strong> ${round(avg_ticket, 2)}</li>
        </ul>

        <h2>📈 Comparación Semanal</h2>
        <p><strong>Ventas Semana Anterior:</strong> ${round(total_prev, 2)}</p>
        <p><strong>Variación:</strong> {variation}% — {trend_text}</p>

        <h2>🧠 Recomendación Estratégica</h2>
        <p>{decision}</p>
        """

        self.write({
            'analysis_result': message
        })

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }