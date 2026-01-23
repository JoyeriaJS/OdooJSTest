/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Gui } from "@web/gui/gui";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { rpc } from "@web/core/network/rpc_service";
import { PosComponent } from "@point_of_sale/app/components/pos_component/pos_component";
import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";

export class DiscountButton extends PosComponent {
    setup() {
        super.setup();
        this.pos = usePos();
    }

    async click() {
        const { confirmed, payload } = await Gui.showPrompt({
            title: "Código de descuento",
            body: "Ingrese un código autorizado:",
        });

        if (!confirmed) return;

        const code = payload.trim().toUpperCase();

        const result = await rpc("/web/dataset/call_kw", {
            model: "pos.discount.code",
            method: "search_read",
            args: [[["code", "=", code]], ["code", "discount_type", "discount_value", "used", "expired"]],
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

DiscountButton.template = "DiscountButtonTemplate";

// Patch para insertar botón en PaymentScreen
patch(PaymentScreen.prototype, "pos_discount_authorized", {
    get addDiscountButton() {
        return true;
    }
});

// Agregar a la ActionPad
registry.category("pos_screens").add("discount_button", {
    Component: DiscountButton,
    position: "payment-buttons",
});
