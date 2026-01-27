/** @odoo-module **/

import { NumberPopup } from "@point_of_sale/app/popup/number_popup/number_popup";
import { patch } from "@web/core/utils/patch";
import { DiscountButton } from "@point_of_sale/app/screens/product_screen/control_buttons/discount_button";
import { useService } from "@web/core/utils/hooks";

patch(DiscountButton.prototype, "pos_discount_authorized", {

    setup() {
        super.setup();
        this.rpc = useService("rpc");
        this.dialog = useService("dialog");
    },

    async onClick() {

        // 1️⃣ Pedir código primero
        const { confirmed, value } = await this.dialog.prompt({
            title: "Código Autorizado",
            body: "Ingrese el código de descuento:"
        });

        if (!confirmed) return;

        const code = value.trim().toUpperCase();

        // 2️⃣ Validar código en el backend
        const result = await this.rpc("/web/dataset/call_kw", {
            model: "pos.discount.code",
            method: "search_read",
            args: [[["code", "=", code]], ["discount_value", "discount_type", "used", "expired"]],
        });

        if (!result.length) {
            this.dialog.alert("Código no válido.");
            return;
        }

        const data = result[0];

        if (data.used || data.expired) {
            this.dialog.alert("Código ya usado o expirado.");
            return;
        }

        // 3️⃣ Mostrar popup original pero limitado al valor del código
        const discount = await this.showPopup(NumberPopup, {
            title: "Aplicar descuento autorizado",
            startingValue: data.discount_value,
        });

        if (!discount.confirmed) return;

        const qty = discount.payload;

        if (qty !== data.discount_value) {
            this.dialog.alert("El porcentaje/monto debe coincidir EXACTAMENTE con el autorizado.");
            return;
        }

        // 4️⃣ Continuar con la lógica original
        return super.onClick();
    },
});
