from odoo import models, api
from collections import defaultdict
from odoo.exceptions import AccessError

class ReportStockTransferCharge(models.AbstractModel):
    _name = 'report.stock_transfer_charge_report.stock_transfer_charge_report_template'
    _description = 'Reporte General de Traspasos'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not self.env.user.has_group('base.group_system'):
            raise AccessError("Sólo los administradores pueden generar este reporte.")

        pickings = self.env['stock.picking'].browse(docids) if docids else self.env['stock.picking'].search([])
        pickings = pickings or self.env['stock.picking']

        # Buscar la pricelist "Interno (CLP)" o "Interno"
        pricelist = self.env['product.pricelist'].search([
            ('name', 'ilike', 'Interno')
        ], limit=1)
        productos_precio_interno = {}
        for picking in pickings:
            for ml in picking.move_line_ids_without_package:
                product = ml.product_id
                if not product:
                    continue
                if product.id in productos_precio_interno:
                    continue
                precio_interno = 0.0
                if pricelist:
                    item = self.env['product.pricelist.item'].search([
                        ('pricelist_id', '=', pricelist.id),
                        ('product_tmpl_id', '=', product.product_tmpl_id.id),
                        ('applied_on', '=', '1_product'),
                    ], limit=1)
                    if item:
                        precio_interno = item.fixed_price
                productos_precio_interno[product.id] = precio_interno

        # Agrupar para el resumen
        resumen = defaultdict(lambda: defaultdict(lambda: {'total': 0.0, 'traspasos': []}))
        for picking in pickings:
            fecha = picking.date_done
            if not fecha:
                continue
            mes = fecha.strftime('%B %Y')
            origen = picking.location_id.display_name
            destino = picking.location_dest_id.display_name
            subtotal = 0.0
            productos = []
            for ml in picking.move_line_ids_without_package:
                precio_interno = productos_precio_interno.get(ml.product_id.id, 0.0)
                linea_total = ml.quantity * precio_interno
                subtotal += linea_total
                productos.append({
                    'producto': ml.product_id.display_name,
                    'cantidad': ml.quantity,
                    'uom': ml.product_uom_id.name,
                    'precio_interno': precio_interno,
                    'peso': ml.product_id.weight or 0.0,
                    'linea_total': linea_total
                })
            if subtotal > 0:
                resumen[mes][origen]['total'] += subtotal
                resumen[mes][origen]['traspasos'].append({
                    'nombre': picking.name,
                    'destino': destino,
                    'usuario': picking.create_uid.name,
                    'fecha': fecha.strftime('%d/%m/%Y %H:%M:%S'),
                    'productos': productos,
                    'subtotal': subtotal
                })

        # Pasar resumen listo como lista ordenada
        resumen_mensual = []
        for mes, origenes in sorted(resumen.items()):
            for origen, data in origenes.items():
                resumen_mensual.append({
                    'mes': mes,
                    'origen': origen,
                    'total': round(data['total'], 2),
                    'traspasos': data['traspasos'],
                })

        return {
            'doc_ids': pickings.ids,
            'doc_model': 'stock.picking',
            'docs': pickings,
            'resumen_mensual': resumen_mensual,
        }
