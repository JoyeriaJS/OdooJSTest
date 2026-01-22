/** @odoo-module **/

import { registry } from "@web/core/registry";
import { PosComponent } from "@point_of_sale/app/components/pos_component/pos_component";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { TextInputPopup } from "@point_of_sale/app/utils/input_popups/input_popups";
import { ConfirmPopup } from "@point_of_sale/app/utils/confirm_popup/confirm_popup";
import { ErrorPopup } from "@point_of_sale/app/utils/error_popup/error_popup";
import rpc from "web.rpc";

export class DiscountButton extends PosComponent {
    setup() {
        super.setup();
        this.pos = usePos();
    }

    async onClick() {
        const { confirmed, payload } = await this.pos.popup.add(TextInputPopup, {
            title: "Ingrese código de descuento",
        });

        if (!confirmed) return;

        const code = payload.trim();

        const result = await rpc.query({
            model: "pos.discount.code",
            method: "search_read",
            args: [
                [["code", "=", code]],
                ["code", "discount_type", "discount_value", "used", "expired"],
            ],
        });

        if (!result.length) {
            return this.pos.popup.add(ErrorPopup, {
                title: "Código inválido",
                body: "El código no existe.",
            });
        }

        const data = result[0];

        if (data.used || data.expired) {
            return this.pos.popup.add(ErrorPopup, {
                title: "No válido",
                body: "El código ya fue usado o expiró.",
            });
        }

        const order = this.pos.get_order();

        if (data.discount_type === "percent") {
            order.add_global_discount(data.discount_value);
        } else {
            order.add_paymentline(this.pos.cashRegister, -data.discount_value);
        }

        await rpc.query({
            model: "pos.discount.code",
            method: "write",
            args: [[data.id], { used: true, fecha_uso: new Date() }],
        });

        this.pos.popup.add(ConfirmPopup, {
            title: "Descuento aplicado",
            body: "El código fue aplicado correctamente.",
        });
    }
}

DiscountButton.template = "DiscountButtonTemplate";

registry.category("pos_components").add("DiscountButton", DiscountButton);
