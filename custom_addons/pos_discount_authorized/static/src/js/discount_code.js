/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Gui } from "@web/gui/gui";
import rpc from "@web/core/network/rpc_service";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Component } from "@odoo/owl";

export class DiscountButton extends Component {
    static template = "DiscountButtonTemplate";

    setup() {
        this.pos = usePos();
    }

    async click() {
        const { confirmed, payload } = await Gui.showPrompt({
            title: "Código de descuento",
            body: "Ingrese código autorizado:",
        });

        if (!confirmed) return;

        const code = payload.trim().toUpperCase();

        const result = await rpc("/web/dataset/call_kw", {
            model: "pos.discount.code",
            method: "search_read",
            args: [
                [["code", "=", code]],
                ["code", "discount_type", "discount_value", "used", "expired"],
            ],
        });

        if (!result.length) {
            Gui.showError("Código no existe");
            return;
        }

        const data = result[0];

        if (data.used || data.expired) {
            Gui.showError("Código usado o expirado");
            return;
        }

        const order = this.pos.get_order();

        let amount = 0;

        if (data.discount_type === "percent") {
            amount = -(order.get_total_with_tax() * (data.discount_value / 100));
        } else {
            amount = -data.discount_value;
        }

        order.add_product(
            this.pos.db.get_product_by_id(this.pos.config.discount_product_id),
            { price: amount }
        );

        await rpc("/web/dataset/call_kw", {
            model: "pos.discount.code",
            method: "write",
            args: [[data.id], { used: true, fecha_uso: new Date() }],
        });

        Gui.showNotification("Descuento aplicado");
    }
}

registry.category("pos_ui").add("discount_button", DiscountButton);
