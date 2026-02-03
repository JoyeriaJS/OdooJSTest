/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Order } from "@point_of_sale/app/models/pos_model";

patch(Order.prototype, {
    async set_discount(discount) {

        // Permitir descuentos hasta 10%
        if (discount <= 10) {
            return super.set_discount(discount);
        }

        // Popup nativo del navegador (funciona en cualquier POS)
        const codigo = window.prompt("Descuento mayor al 10%. Ingrese código de autorización:");

        if (!codigo) {
            alert("Operación cancelada.");
            return;
        }

        // Llamar al backend
        const valido = await this.pos.rpc({
            model: "pos.discount.authcode",
            method: "validar_codigo",
            args: [[], codigo, this.pos.get_cashier().id],
        });

        if (!valido) {
            alert("Código inválido o expirado.");
            return;
        }

        // Si está válido → aplicar descuento
        return super.set_discount(discount);
    },
});
