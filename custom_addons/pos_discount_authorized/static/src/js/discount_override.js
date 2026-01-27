/** @odoo-module **/

import { DiscountButton } from "@point_of_sale/app/screens/product_screen/control_buttons/discount_button";

const originalFunction = DiscountButton.prototype.onClick;

DiscountButton.prototype.onClick = async function () {
    const dialog = this.env.services.dialog;
    const rpc = this.env.services.rpc;

    // 1. Solicitar código antes del descuento
    const { confirmed, value } = await dialog.prompt({
        title: "Autorización requerida",
        body: "Ingrese código autorizado:",
    });

    if (!confirmed || !value) {
        return; // Usuario canceló → NO sigue a descuento
    }

    const code = value.trim().toUpperCase();

    // 2. Validar código en tu modelo de autorización
    const result = await rpc("/web/dataset/call_kw", {
        model: "pos.discount.code",
        method: "search_read",
        args: [[["code", "=", code]], ["discount_value", "discount_type", "used", "expired"]],
    });

    if (!result.length) {
        await dialog.alert("Código no válido");
        return;
    }

    const data = result[0];

    if (data.used || data.expired) {
        await dialog.alert("Código ya utilizado o expirado");
        return;
    }

    // 3. Marcar como usado
    await rpc("/web/dataset/call_kw", {
        model: "pos.discount.code",
        method: "write",
        args: [[data.id], { used: true, fecha_uso: new Date() }],
    });

    // 4. Guardar porcentaje autorizado (para aplicar)
    const authorizedPercent =
        data.discount_type === "percent" ? data.discount_value : null;

    if (!authorizedPercent) {
        dialog.alert("Solo se permiten códigos de tipo porcentaje");
        return;
    }

    // 5. Llamar al popup ORIGINA‌‍L de descuento pero con porcentaje ya definido
    const order = this.env.pos.get_order();

    // Aplicar descuento directamente sin mostrar popup
    order.set_discount(authorizedPercent);

    await dialog.alert(`Descuento autorizado: ${authorizedPercent}% aplicado exitosamente.`);
};
