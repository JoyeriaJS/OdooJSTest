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

        resumen = defaultdict(lambda: defaultdict(float))
        for picking in pickings:
            fecha = picking.date_done
            if not fecha:
                continue
            mes = fecha.strftime('%B %Y')
            origen = picking.location_id.display_name
            for ml in picking.move_line_ids_without_package:
                precio_interno = getattr(ml.product_id, 'costo_interno', 0.0)
                peso = getattr(ml.product_id, 'weight', 0.0)
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
            'docs': pickings,
            'resumen_mensual': resumen_listo,
        }
