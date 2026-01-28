/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class DiscountButton extends Component {
    static template = "DiscountButtonTemplate";

    setup() {
        this.dialog = useService("dialog");
        this.pos = usePos();
    }

    async onClick() {
        const { confirmed, value } = await this.dialog.prompt({
            title: "Código de descuento",
            body: "Ingrese el código autorizado:"
        });

        if (!confirmed) return;

        const code = value.trim();

        const result = await this.pos.rpc({
            model: "pos.discount.code",
            method: "search_read",
            args: [[["code", "=", code]], ["code","discount_type","discount_value","used","expired"]],
        });

        if (!result.length) {
            return this.dialog.alert("Código no válido.");
        }

        const data = result[0];

        if (data.used || data.expired) {
            return this.dialog.alert("El código ya fue usado o está expirado.");
        }

        const order = this.pos.get_order();
        let amount = 0;

        if (data.discount_type === "percent") {
            amount = -(order.get_total_with_tax() * (data.discount_value / 100));
        } else {
            amount = -data.discount_value;
        }

        const discountProduct = this.pos.db.get_product_by_id(this.pos.config.discount_product_id);

        order.add_product(discountProduct, { price: amount });

        await this.pos.rpc({
            model: "pos.discount.code",
            method: "write",
            args: [[data.id], { used: true }],
        });

        this.dialog.alert("Descuento aplicado correctamente.");
    }
}

registry.category("pos_actionpad_buttons").add(
    "discount_authorized_button",
    { component: DiscountButton, position: 99 }
);
