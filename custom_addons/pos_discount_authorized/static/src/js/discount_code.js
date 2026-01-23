/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Gui } from "@web/gui/gui";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Component } from "@odoo/owl";

class DiscountButton extends Component {
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

        // Buscar código en backend
        const result = await this.pos.orm.call(
            "pos.discount.code",
            "search_read",
            [[["code", "=", code]], ["code", "discount_type", "discount_value", "used", "expired"]]
        );

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
        let discountAmount = 0;

        if (data.discount_type === "percent") {
            discountAmount = -(order.get_total_with_tax() * (data.discount_value / 100));
        } else {
            discountAmount = -data.discount_value;
        }

        const product = this.pos.db.get_product_by_id(this.pos.config.discount_product_id);

        if (!product) {
            Gui.showError("⚠️ No hay producto de descuento configurado en el POS.");
            return;
        }

        order.add_product(product, { price: discountAmount });

        await this.pos.orm.call("pos.discount.code", "write", [
            [data.id],
            {
                used: true,
                fecha_uso: new Date(),
            },
        ]);

        Gui.showNotification("Descuento aplicado correctamente");
    }
}

DiscountButton.template = "DiscountButtonTemplate";

registry.category("pos_ui").add("DiscountButton", DiscountButton);
