/** @odoo-module **/

import { PosComponent } from "@point_of_sale/app/components/pos_component/pos_component";
import { registry } from "@web/core/registry";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class PosDiscountButton extends PosComponent {
    setup() {
        this.pos = usePos();
        console.log("🔥 POS DISCOUNT MODULE LOADED OK");
    }

    async onClick() {
        const code = prompt("Ingrese código:");

        if (!code) return;

        const result = await this.pos.env.services.rpc("/web/dataset/call_kw", {
            model: "pos.discount.code",
            method: "search_read",
            args: [[["code", "=", code.toUpperCase()]]],
            kwargs: { fields: ["discount_type", "discount_value", "used", "expired"] },
        });

        if (!result.length) {
            alert("Código no existe");
            return;
        }

        const data = result[0];

        if (data.used || data.expired) {
            alert("Código usado o expirado");
            return;
        }

        const order = this.pos.get_order();
        let amount = 0;

        if (data.discount_type === "percent") {
            amount = -(order.get_total_with_tax() * (data.discount_value / 100));
        } else {
            amount = -data.discount_value;
        }

        order.add_product(this.pos.config.discount_product_id, { price: amount });

        await this.pos.env.services.rpc("/web/dataset/call_kw", {
            model: "pos.discount.code",
            method: "write",
            args: [[data.id], { used: true }],
        });

        alert("Descuento aplicado.");
    }
}

PosDiscountButton.template = "PosDiscountButton";

registry.category("pos_screens").add("PosDiscountButton", {
    component: PosDiscountButton,
    position: "payment-buttons",
});
