/** @odoo-module **/

import { PosComponent } from "@point_of_sale/app/components/pos_component/pos_component";
import { registry } from "@web/core/registry";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class PosDiscountButton extends PosComponent {
    setup() {
        this.pos = usePos();
        console.log("🔥 POS BUTTON LOADED CORRECTLY");
    }

    async onClick() {
        const { confirmed, payload } = await this.env.services.popup.show("NumberPopup", {
            title: "Ingrese código autorizado",
            startingValue: "",
            confirmText: "Validar",
        });

        if (!confirmed) return;

        const code = payload;

        const result = await this.rpc({
            model: "pos.discount.code",
            method: "validate_code",
            args: [code],
        });

        if (!result.valid) {
            this.env.services.popup.add("ErrorPopup", {
                title: "Código inválido",
                body: result.message,
            });
            return;
        }

        // Aplicar descuento
        const order = this.pos.get_order();

        if (result.type === "percent") {
            order.add_product(this.pos.db.get_product_by_id(result.product_id), {
                price: -order.get_total_with_tax() * (result.value / 100),
            });
        } else {
            order.add_product(this.pos.db.get_product_by_id(result.product_id), {
                price: -result.value,
            });
        }

        this.env.services.popup.show("ConfirmPopup", {
            title: "Descuento aplicado",
            body: `Código válido. Descuento aplicado exitosamente.`,
        });
    }
}

PosDiscountButton.template = "PosDiscountButton";

registry.category("pos_product_buttons").add("PosDiscountButton", {
    component: PosDiscountButton,
    position: "after",
});
