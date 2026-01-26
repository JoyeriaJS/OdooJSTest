/** @odoo-module **/

import { registry } from "@web/core/registry";
import { PosComponent } from "@point_of_sale/app/components/pos_component/pos_component";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";

export class DiscountButton extends PosComponent {
    setup() {
        super.setup();
        this.pos = usePos();
        this.popup = useService("popup");
    }

    async onClick() {
        const { confirmed, payload } = await this.popup.add({
            type: "text",
            title: "Código de descuento",
            body: "Ingrese un código autorizado:",
        });

        if (!confirmed) return;

        const code = payload.trim().toUpperCase();

        const result = await this.pos.rpc({
            model: "pos.discount.code",
            method: "search_read",
            args: [[["code", "=", code]], ["code", "discount_type", "discount_value", "used", "expired"]],
        });

        if (!result.length) {
            await this.popup.add({
                type: "alert",
                title: "Error",
                body: "Código no existe",
            });
            return;
        }

        const data = result[0];

        if (data.used || data.expired) {
            await this.popup.add({
                type: "alert",
                title: "Código inválido",
                body: "Código usado o expirado",
            });
            return;
        }

        const order = this.pos.get_order();
        let amount = 0;

        if (data.discount_type === "percent") {
            amount = -(order.get_total_with_tax() * (data.discount_value / 100));
        } else {
            amount = -data.discount_value;
        }

        const discount_prod = this.pos.db.get_product_by_id(this.pos.config.discount_product_id);

        order.add_product(discount_prod, { price: amount });

        await this.pos.rpc({
            model: "pos.discount.code",
            method: "write",
            args: [[data.id], { used: true, fecha_uso: new Date() }],
        });

        await this.popup.add({
            type: "alert",
            title: "Éxito",
            body: "Descuento aplicado",
        });
    }
}

DiscountButton.template = "DiscountButtonTemplate";

// Registrar botón en ActionPad
registry.category("pos_actionpad_buttons").add("DiscountButton", {
    component: DiscountButton,
});
