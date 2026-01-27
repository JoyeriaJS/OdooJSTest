/** @odoo-module **/

import { DiscountButton } from "@point_of_sale/app/screens/product_screen/control_buttons/discount_button";

const patch = DiscountButton.prototype.onClick;

DiscountButton.prototype.onClick = async function () {
    const dialog = this.env.services.dialog;
    const rpc = this.env.services.rpc;

    // Pedir código de autorización
    const { confirmed, value } = await dialog.prompt({
        title: "Código Autorizador",
        body: "Ingrese el código autorizado para aplicar el descuento:",
    });

    if (!confirmed || !value) {
        return; // Usuario canceló → NO aplica el descuento
    }

    const code = value.trim().toUpperCase();

    // Verificar contra nuestro modelo
    const result = await rpc("/web/dataset/call_kw", {
        model: "pos.discount.code",
        method: "search_read",
        args: [[["code", "=", code]], ["used", "expired"]],
    });

    if (!result.length) {
        dialog.alert("Código inválido");
        return;
    }

    const data = result[0];

    if (data.used || data.expired) {
        dialog.alert("Código ya utilizado o expirado");
        return;
    }

    // Marcar código como usado
    await rpc("/web/dataset/call_kw", {
        model: "pos.discount.code",
        method: "write",
        args: [[data.id], { used: true, fecha_uso: new Date() }],
    });

    // Si todo es OK → ejecutar función original del botón
    return patch.apply(this, arguments);
};
