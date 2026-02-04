from odoo import api, SUPERUSER_ID

def restore_direccion_entrega(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    Reparacion = env["joyeria.reparacion"]
    reparaciones = Reparacion.search([])

    # Mapa de direcciones estándar por tienda
    DIRECCIONES_TIENDAS = {
        "local 345": "Paseo Estado 344, Local 345, Santiago Centro, Metro Plaza de Armas (Galería Pasaje Matte)",
        "local 906": "Paseo Estado 344, Local 906, Santiago Centro, Metro Plaza de Armas (Galería Pasaje Matte)",
        "local 392": "Paseo Estado 344, Local 392, Santiago Centro, Metro Plaza de Armas (Galería Pasaje Matte)",
        "local 329": "Paseo Estado 344, Local 329, Santiago Centro, Metro Plaza de Armas (Galería Pasaje Matte)",
        "local 325": "Paseo Estado 344, Local 325, Santiago Centro, Metro Plaza de Armas (Galería Pasaje Matte)",
        "local 383 online": "Paseo Estado 344, Local 383 Online, Santiago Centro, Metro Plaza de Armas (Galería Pasaje Matte)",
        "local 921": "Paseo Estado 344, Local 921, Santiago Centro, Metro Plaza de Armas (Galería Pasaje Matte)",
        "local 584": "Monjitas 873, Local 584, Santiago Centro, Metro Plaza de Armas",
        "local maipu": "Jumbo, Av. Los Pajaritos 3302 (Local Maipú), Metro Santiago Bueras",
    }

    for rec in reparaciones:
        # No sobreescribir si ya tiene dirección válida
        if rec.direccion_entrega:
            continue

        # Si tiene tienda → aplicar dirección estándar
        if rec.local_tienda in DIRECCIONES_TIENDAS:
            rec.direccion_entrega = DIRECCIONES_TIENDAS[rec.local_tienda]
            continue

        # Si tiene cliente → usar dirección del cliente
        if rec.cliente_id and rec.cliente_id.street:
            rec.direccion_entrega = rec.cliente_id.street
            continue

        # Si no se puede deducir → dejar vacío para revisión manual
        rec.direccion_entrega = ""
