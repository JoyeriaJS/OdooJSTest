/** @odoo-module **/

import { registry } from "@web/core/registry";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";

console.warn("🔥 POS DISCOUNT MODULE LOADED CORRECTLY 🔥");

export class DiscountAuthButton extends Component {
    setup() {
        this.pos = usePos();
        this.dialog = useService("dialog");
    }

    async onClick() {
        console.warn("🔥 CLICK EN BOTÓN DE DESCUENTO AUTORIZADO");

        const { confirmed, value } = await this.dialog.prompt({
            title: "Autorización de descuento",
            body: "Ingrese código autorizado:"
        });

        if (!confirmed) {
            return;
        }

        const code = value.trim().toUpperCase();

        // Consulta RPC
        const result = await this.pos.env.services.rpc("/web/dataset/call_kw", {
            model: "pos.discount.code",
            method: "search_read",
            args: [[["code", "=", code]], ["code", "discount_type", "discount_value", "used", "expired"]],
        });

        if (!result.length) {
            this.dialog.alert("Código no existe");
            return;
        }

        const data = result[0];

        if (data.used || data.expired) {
            this.dialog.alert("Código usado o expirado");
            return;
        }

        // Guardamos para usarlo en el popup real del POS
        this.pos.global_discount_info = data;

        this.dialog.alert(`Código válido. Se autorizó un descuento de: ${data.discount_value}`);

        // aquí después enganchamos el popup nativo
    }
}

DiscountAuthButton.template = "DiscountAuthButtonTemplate";

registry.category("pos_screens").add("DiscountAuthButton", {
    component: DiscountAuthButton,
    position: "payment-buttons"
});
