{
    'name': 'Reparaciones de Joyería',
    'version': '1.0',
    'summary': 'Gestión de órdenes de reparación de joyas',
    'author': 'DR',
    'category': 'Operations',

    'depends': [
        'base',
        'product',
        'sale',
        'contacts',
        'point_of_sale',
        'report_xlsx',
        'mail',
    ],

    'data': [
        # 🔹 DATA BASE (no depende de nada)
        'data/ir_sequence_data.xml',
        'data/joyeria_data.xml',

        # 🔹 VISTAS (esto fuerza carga del modelo primero)
        'views/reparacion_js.xml',
        'views/vendedora_views.xml',
        'views/trabajadores_views.xml',
        'views/reparacion_confirm_view.xml',

     

        # 🔹 SECURITY (DESPUÉS de que el modelo existe)
        'security/ir.model.access.csv',
        'security/joyeria_security.xml',

        # 🔹 REPORTES (al final siempre)
        'report/report.xml',
        'report/report_qrcode_template.xml',
        'report/reporte_responsable_report.xml',
        'report/reporte_reparaciones_responsable.xml',
        'report/report_actions.xml',
        'report/report_etiqueta_usuario.xml',
        'report/report_etiqueta_vendedora.xml',

        'report/report_salida_taller_xlsx.xml',
        'report/report_sales_by_store_xlsx.xml',
        'report/report_sales_by_vendedora_xlsx.xml',

        'report/reporte_salida_taller_report_action.xml',
        'report/reporte_salida_taller_templates.xml',
        'report/report_sales_by_store.xml',
        'report/report_sales_by_store_template.xml',
        'report/report_sales_by_vendedora.xml',
        'report/report_sales_by_vendedora_template.xml',

        'report/report_monthly_rma_pos_action.xml',
        'report/report_monthly_rma_pos_template.xml',
    ],

    # 🔥 JS BIEN CARGADO
    'assets': {
        'web.assets_backend': [
            'joyeria_reparaciones/static/src/reparacion_form.js',
        ],
    },

    'installable': True,
    'application': True,
}