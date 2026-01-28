/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";

export class DiscountButton extends Component {
    static template = "DiscountButtonTemplate";

    setup() {
        this.pos = usePos();
        this.dialog = useService("dialog");
    }

    async onClick() {
        const { confirmed, value } = await this.dialog.prompt({
            title: "Código de descuento",
            body: "Ingrese un código autorizado:",
        });

        if (!confirmed) return;

        const code = value.trim().toUpperCase();

        // Validación backend
        const result = await this.pos.rpc({
            model: "pos.discount.code",
            method: "search_read",
            args: [[["code", "=", code]], ["code", "discount_type", "discount_value", "used", "expired"]],
        });

        if (!result.length) {
            return this.dialog.alert("Código no existe");
        }

        const data = result[0];
        if (data.used || data.expired) {
            return this.dialog.alert("Código usado o expirado");
        }

        // Aplicar descuento
        const order = this.pos.get_order();
        let amount = 0;

        if (data.discount_type === "percent") {
            amount = -(order.get_total_with_tax() * (data.discount_value / 100));
        } else {
            amount = -data.discount_value;
        }

        const discountProduct = this.pos.db.get_product_by_id(this.pos.config.discount_product_id);

        order.add_product(discountProduct, {
            price: amount,
        });

        // Marcar como usado
        await this.pos.rpc({
            model: "pos.discount.code",
            method: "write",
            args: [[data.id], { used: true, fecha_uso: new Date() }],
        });

        this.dialog.alert("Descuento aplicado correctamente");
    }
}

// REGISTRO CORRECTO DEL BOTÓN
registry.category("pos_actionpad_buttons").add("discount_authorized_button", {
    component: DiscountButton,
    position: 90,
});
