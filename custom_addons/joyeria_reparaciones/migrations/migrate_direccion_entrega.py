def migrate_direccion_entrega(cr):
    """
    Convierte valores del antiguo campo Selection -> valores de texto (Char)
    antes de que el módulo se actualice. Esto evita errores de ondelete en Odoo.
    """

    mapping = {
        'local 345': 'Paseo Estado 344, Local 345, Santiago Centro, Metro Plaza de Armas (Galería Pasaje Matte)',
        'local 906': 'Paseo Estado 344, Local 906, Santiago Centro, Metro Plaza de Armas (Galería Pasaje Matte)',
        'local 392': 'Paseo Estado 344, Local 392, Santiago Centro, Metro Plaza de Armas (Galería Pasaje Matte)',
        'local 329': 'Paseo Estado 344, Local 329, Santiago Centro, Metro Plaza de Armas (Galería Pasaje Matte)',
        'local 325': 'Paseo Estado 344, Local 325, Santiago Centro, Metro Plaza de Armas (Galería Pasaje Matte)',
        'local 383 online': 'Paseo Estado 344, Local 383 Online, Santiago Centro, Metro Plaza de Armas (Galería Pasaje Matte)',
        'local 921': 'Paseo Estado 344, Local 921, Santiago Centro, Metro Plaza de Armas (Galería Pasaje Matte)',
        'local 584': 'Monjitas 873, Local 584, Santiago Centro, Metro Plaza de Armas',
        'local maipu': 'Jumbo, Av. Los Pajaritos 3302 (Local Maipú), Metro Santiago Bueras',
    }

    # Convierte los valores antiguos al texto final
    for old, new in mapping.items():
        cr.execute("""
            UPDATE joyeria_reparacion
            SET direccion_entrega = %s
            WHERE direccion_entrega = %s
        """, (new, old))
