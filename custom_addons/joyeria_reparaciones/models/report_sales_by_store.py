class ReportSalesByStore(models.AbstractModel):
    _name = 'report.joyeria_reparaciones.report_sales_by_store_template'
    _description = 'Ventas por Tienda y Mes (por Fecha de Firma)'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Permisos...
        if not self.env.user.has_group('base.group_system'):
            raise AccessError("Sólo los administradores pueden generar este reporte.")
        # Datos de wizard (si no vienen, poner por defecto)
        precio_oro_amarillo = data.get('precio_oro_amarillo') if data else 160000.0
        precio_oro_rosado = data.get('precio_oro_rosado') if data else 150000.0

        docs = self.env['joyeria.reparacion'].browse(docids).filtered(lambda r: r.fecha_firma)
        groups = OrderedDict()
        for rec in docs:
            store = rec.local_tienda or 'Sin Tienda'
            dt = rec.fecha_firma
            key = (store, dt.year, dt.month)
            if key not in groups:
                groups[key] = {
                    'store': store,
                    'year': dt.year,
                    'month': dt.month,
                    'docs': [],
                    'sums': {
                        'peso_valor':        0.0,
                        'metales_extra':     0.0,
                        'precio_unitario':   0.0,
                        'extra':             0.0,
                        'extra2':            0.0,
                        'saldo':             0.0,
                        'cobro_interno':     0.0,
                        'hechura':           0.0,
                        'cobros_extras':     0.0,
                        'rosado_value':      0.0,
                        'amarillo_value':    0.0,
                        'total_metales':     0.0,
                        'pago_taller':       0.0,
                    }
                }
            grp = groups[key]

            w_val = rec.peso_valor or 0.0
            w_ext = rec.metales_extra or 0.0
            val_rosado   = 0.0
            val_amarillo = 0.0

            total_weight = w_val + w_ext
            if rec.metal_utilizado == 'oro 18k rosado':
                val_rosado = total_weight * precio_oro_rosado
            elif rec.metal_utilizado == 'oro 18k amarillo':
                val_amarillo = total_weight * precio_oro_amarillo

            total_metales = val_rosado + val_amarillo

            saldo = (rec.precio_unitario or 0.0) + (rec.extra or 0.0) - (rec.abono or 0.0)
            pago_taller = total_metales + \
                          (rec.cobro_interno or 0.0) + \
                          (rec.hechura or 0.0) + \
                          (rec.cobros_extras or 0.0)

            grp['docs'].append({
                'rec': rec,
                'peso_valor':       w_val,
                'metales_extra':    w_ext,
                'saldo':            saldo,
                'rosado_value':     val_rosado,
                'amarillo_value':   val_amarillo,
                'total_metales':    total_metales,
                'pago_taller':      pago_taller,
            })

            s = grp['sums']
            s['peso_valor']        += w_val
            s['metales_extra']     += w_ext
            s['precio_unitario']   += rec.precio_unitario or 0.0
            s['extra']             += rec.extra or 0.0
            s['extra2']            += rec.extra2 or 0.0
            s['saldo']             += saldo
            s['cobro_interno']     += rec.cobro_interno or 0.0
            s['hechura']           += rec.hechura or 0.0
            s['cobros_extras']     += rec.cobros_extras or 0.0
            s['rosado_value']      += val_rosado
            s['amarillo_value']    += val_amarillo
            s['total_metales']     += total_metales
            s['pago_taller']       += pago_taller

        return {
            'doc_ids':   docids,
            'doc_model': 'joyeria.reparacion',
            'groups':    list(groups.values()),
        }
