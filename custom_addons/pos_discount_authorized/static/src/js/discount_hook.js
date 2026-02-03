/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Orderline } from "@point_of_sale/app/models/pos_model";
import { useService } from "@web/core/utils/hooks";

patch(Orderline.prototype, {
    async set_discount(discount) {

        // Si el descuento es menor o igual al 10%, dejar pasar normal
        if (discount <= 10) {
            return super.set_discount(discount);
        }

        const popup = useService("popup");

        const { confirmed, payload } = await popup.add({
            type: "text",
            title: "Autorización requerida",
            body: "Este descuento requiere un código:",
            confirmText: "Validar",
            cancelText: "Cancelar",
        });

        if (!confirmed) return;

        const codigo = payload;

        // Llamar al backend
        const result = await this.pos.rpc({
            model: "pos.discount.authcode",
            method: "validar_codigo",
            args: [[], codigo, this.pos.get_cashier().id],
        });

        if (result) {
            return super.set_discount(discount);
        } else {
            await popup.add({
                title: "Código inválido",
                body: "El código ingresado no es válido, está usado o expiró.",
            });
        }
    },
});
