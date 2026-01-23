/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Gui } from "@web/gui/gui";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Component } from "@odoo/owl";

class DiscountButton extends Component {
    static template = "DiscountButtonTemplate";

    setup() {
        this.pos = usePos();
    }

    async click() {
        const { confirmed, payload } = await Gui.showPrompt({
            title: "Código de descuento",
            body: "Ingrese un código autorizado:",
        });

        if (!confirmed) return;

        const code = payload.trim().toUpperCase();

        const result = await this.pos.orm.call(
            "pos.discount.code",
            "search_read",
            [[["code", "=", code]], ["code", "discount_type", "discount_value", "used", "expired"]]
        );

        if (!result.length) {
            return Gui.showError("Código no existe");
        }

        const data = result[0];

        if (data.used || data.expired) {
            return Gui.showError("Código usado o expirado");
        }

        const order = this.pos.get_order();
        let amount = 0;

        if (data.discount_type === "percent") {
            amount = -(order.get_total_with_tax() * (data.discount_value / 100));
        } else {
            amount = -data.discount_value;
        }

        const discountProduct = this.pos.db.get_product_by_id(this.pos.config.discount_product_id);

        if (!discountProduct) {
            return Gui.showError("No hay producto configurado para descuentos");
        }

        order.add_product(discountProduct, { price: amount });

        await this.pos.orm.call("pos.discount.code", "write", [
            [data.id],
            { used: true, fecha_uso: new Date() },
        ]);

        Gui.showNotification("Descuento aplicado");
    }
}

registry.category("pos_ui").add("DiscountButton", DiscountButton);
