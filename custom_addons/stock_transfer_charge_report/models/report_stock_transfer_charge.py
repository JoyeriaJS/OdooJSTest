from odoo import models, api, fields
from collections import defaultdict
from datetime import datetime

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte de Traspasos Internos por Mes y Producto'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Todos los pickings seleccionados, o todos los de tipo interno
        pickings = self.env['stock.picking'].browse(docids) if docids else self.env['stock.picking'].search([('picking_type_code', '=', 'internal')])
        pricelist = self.env['product.pricelist'].search([('name', '=', 'Interno (CLP)')], limit=1)
        
        # Diccionario para agrupación: {(mes, año, producto_id, origen, destino): {datos}}
        agrupados = defaultdict(lambda: {'cantidad': 0.0, 'peso': 0.0, 'subtotal': 0.0, 'origen': '', 'destino': '', 'producto': None, 'precio_interno': 0.0, 'mes': 0, 'ano': 0})

        # Calcular precios internos
        precios_interno = {}
        if pricelist:
            for producto in pickings.mapped('move_line_ids_without_package.product_id'):
                item = self.env['product.pricelist.item'].search([
                    ('pricelist_id', '=', pricelist.id),
                    ('product_tmpl_id', '=', producto.product_tmpl_id.id),
                    ('applied_on', '=', '1_product'),
                ], limit=1)
                precios_interno[producto.id] = item.fixed_price if item else 0.0

        peso_total_mes = 0.0

        for p in pickings:
            for ml in p.move_line_ids_without_package:
                fecha = p.scheduled_date or p.date_done or p.create_date
                if not fecha:
                    continue
                fecha = fields.Datetime.to_datetime(fecha)
                mes, ano = fecha.month, fecha.year
                key = (mes, ano, ml.product_id.id, p.location_id.id, p.location_dest_id.id)
                precio = precios_interno.get(ml.product_id.id, ml.product_id.standard_price or 0.0)
                cantidad = ml.qty_done or ml.quantity or 0.0
                peso = ml.product_id.weight * cantidad if ml.product_id.weight else 0.0
                agrupados[key]['cantidad'] += cantidad
                agrupados[key]['peso'] += peso
                agrupados[key]['subtotal'] += cantidad * precio
                agrupados[key]['origen'] = p.location_id.display_name
                agrupados[key]['destino'] = p.location_dest_id.display_name
                agrupados[key]['producto'] = ml.product_id
                agrupados[key]['precio_interno'] = precio
                agrupados[key]['mes'] = mes
                agrupados[key]['ano'] = ano
                peso_total_mes += peso

        # Ordenar por mes, año, producto
        resultado = sorted(agrupados.values(), key=lambda x: (x['ano'], x['mes'], x['producto'].display_name if x['producto'] else ""))

        return {
            'grouped_lines': resultado,
            'peso_total_mes': peso_total_mes,
        }
