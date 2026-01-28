/** @odoo-module */

import { registry } from "@web/core/registry";
import { PosComponent } from "@point_of_sale/app/components/pos_component/pos_component";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";

export class DiscountButton extends PosComponent {
    setup() {
        super.setup();
        this.pos = usePos();
        this.dialog = useService("dialog");
        console.log("🔥 POS DISCOUNT MODULE LOADED CORRECTLY 🔥");
    }

    async onClick() {
        const { confirmed, value } = await this.dialog.prompt({
            title: "Código de descuento",
            body: "Ingrese el código:",
        });

        if (!confirmed) {
            return;
        }

        const code = value.trim().toUpperCase();

        const result = await this.pos.env.services.rpc("/web/dataset/call_kw", {
            model: "pos.discount.code",
            method: "search_read",
            args: [[["code", "=", code]], ["code","discount_type","discount_value","used","expired"]],
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

        const order = this.pos.get_order();
        const discount_product = this.pos.db.get_product_by_id(this.pos.config.discount_product_id);

        let amount = 0;

        if (data.discount_type === "percent") {
            amount = -(order.get_total_with_tax() * (data.discount_value / 100));
        } else {
            amount = -data.discount_value;
        }

        order.add_product(discount_product, { price: amount });

        await this.pos.env.services.rpc("/web/dataset/call_kw", {
            model: "pos.discount.code",
            method: "write",
            args: [[data.id], { used: true, fecha_uso: new Date() }],
        });

        this.dialog.alert("Descuento aplicado");
    }
}

DiscountButton.template = "DiscountButtonTemplate";

registry.category("pos_screens").add("DiscountButton", {
    component: DiscountButton,
    position: "payment-buttons",
});
