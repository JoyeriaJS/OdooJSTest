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
        # Siempre retorna un recordset (vacío si no hay)
        pickings = self.env['stock.picking'].browse(docids) if docids else self.env['stock.picking'].search([])
        pickings = pickings or self.env['stock.picking']

        # ... (resto igual, el código que tú tenías)
        # (NO CAMBIES NADA AQUÍ ABAJO)
        pricelist = self.env['product.pricelist'].search([('name', '=', 'Interno')], limit=1)
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
                    ], limit=1)
                    if item:
                        precio_interno = item.fixed_price
                productos_precio_interno[product.id] = precio_interno

        resumen = defaultdict(lambda: defaultdict(float))
        
        for picking in pickings:
            fecha = picking.date_done
            if not fecha:
                continue
            mes = fecha.strftime('%B %Y')
            origen = picking.location_id.display_name
            for ml in picking.move_line_ids_without_package:
                precio_interno = productos_precio_interno.get(ml.product_id.id, 0.0)
                peso = ml.product_id.weight or 0.0
                subtotal = ml.quantity * (precio_interno + peso)
                resumen[mes][origen] += subtotal

        resumen_listo = []
        for mes, origenes in sorted(resumen.items()):
            for origen, total in origenes.items():
                resumen_listo.append({
                    'mes': mes,
                    'origen': origen,
                    'total': round(total, 2),
                })

        return {
            'doc_ids': pickings.ids,
            'doc_model': 'stock.picking',
            'docs': pickings,  # <-- SIEMPRE debe ser recordset/list
            'resumen_mensual': resumen_listo,
            'precios_interno': productos_precio_interno,
        }
