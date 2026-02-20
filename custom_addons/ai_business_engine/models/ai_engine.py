from odoo import models, fields

class AIBusinessEngine(models.Model):
    _name = 'ai.business.engine'
    _description = 'AI Business Decision Engine'

    analysis_result = fields.Text()

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
            trend_color = "#16a34a"
            trend_text = "📈 Crecimiento fuerte"
            decision = "Recomendación: aumentar inventario en productos de mayor rotación."
        elif variation < -10:
            trend_color = "#dc2626"
            trend_text = "📉 Disminución importante"
            decision = "Recomendación: activar promociones o revisar precios."
        else:
            trend_color = "#f59e0b"
            trend_text = "📊 Estabilidad"
            decision = "Recomendación: mantener estrategia actual y monitorear."

        message = f"""
        <h1 style="margin-bottom:10px;">🤖 AI Business Intelligence</h1>

        <div style="display:flex;gap:20px;margin-bottom:20px;">

            <div style="flex:1;background:#f3f4f6;padding:20px;border-radius:10px;">
                <h3>💰 Ventas Última Semana</h3>
                <p style="font-size:26px;font-weight:bold;">${round(total_last,2)}</p>
            </div>

            <div style="flex:1;background:#f3f4f6;padding:20px;border-radius:10px;">
                <h3>🧾 Órdenes</h3>
                <p style="font-size:26px;font-weight:bold;">{orders_count}</p>
            </div>

            <div style="flex:1;background:#f3f4f6;padding:20px;border-radius:10px;">
                <h3>🎯 Ticket Promedio</h3>
                <p style="font-size:26px;font-weight:bold;">${round(avg_ticket,2)}</p>
            </div>

        </div>

        <div style="background:white;padding:20px;border-radius:10px;border:1px solid #e5e7eb;">
            <h3>📈 Comparación Semanal</h3>
            <p><b>Ventas Semana Anterior:</b> ${round(total_prev,2)}</p>
            <p style="color:{trend_color};font-size:18px;font-weight:bold;">
                Variación: {variation}% — {trend_text}
            </p>
        </div>

        <div style="margin-top:20px;background:#eef2ff;padding:20px;border-radius:10px;">
            <h3>🧠 Recomendación Estratégica</h3>
            <p style="font-size:16px;">{decision}</p>
        </div>
        """

        self.write({
            'analysis_result': message
        })

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }