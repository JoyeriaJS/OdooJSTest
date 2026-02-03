/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Orderline } from "@point_of_sale/app/models/pos_model";
import { useService } from "@web/core/utils/hooks";
console.log("🔥 discount_hook.js CARGADO - ODOO 17");
patch(Orderline.prototype, {
    async set_discount(discount) {

        // Dejar pasar descuentos ≤ 10%
        if (discount <= 10) {
            return super.set_discount(discount);
        }

        // Pedir autorización
        const popup = useService("popup");

        const { confirmed, payload } = await popup.add({
            type: "text",
            title: "Autorización requerida",
            body: "Ingrese el código de autorización:",
            confirmText: "Validar",
            cancelText: "Cancelar",
        });

        if (!confirmed) return;

        const codigo = payload;

        // Validación con backend
        const valido = await this.pos.rpc({
            model: "pos.discount.authcode",
            method: "validar_codigo",
            args: [[], codigo, this.pos.get_cashier().id],
        });

        if (!valido) {
            await popup.add({
                title: "Código inválido",
                body: "El código ingresado no es válido, está usado o expiró.",
            });
            return;
        }

        return super.set_discount(discount);
    },
});
