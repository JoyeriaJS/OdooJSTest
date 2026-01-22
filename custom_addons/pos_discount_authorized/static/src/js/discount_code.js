/** @odoo-module **/

import { PosComponent } from "@point_of_sale/app/components/pos_component/pos_component";
import { registry } from "@web/core/registry";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Gui } from "@web/gui/gui";
import { _rpc } from "@web/core/network/rpc_service";

class DiscountCodeButton extends PosComponent {
    setup() {
        super.setup();
        this.pos = usePos();
    }

    async onClick() {
        const popup = await Gui.showPopup("TextInputPopup", {
            title: "Ingresar código de descuento",
            startingValue: "",
        });

        if (!popup.confirmed) return;

        const codigo = popup.payload.trim();

        const result = await _rpc({
            model: "pos.discount.code",
            method: "search_read",
            args: [
                [["code", "=", codigo]],
                ["code", "discount_type", "discount_value", "used", "expired"],
            ],
        });

        if (result.length === 0) {
            Gui.showPopup("ErrorPopup", {
                title: "Código inválido",
                body: "Este código NO existe.",
            });
            return;
        }

        const data = result[0];

        if (data.used || data.expired) {
            Gui.showPopup("ErrorPopup", {
                title: "Código inválido",
                body: "El código está USADO o EXPIRADO.",
            });
            return;
        }

        const order = this.pos.get_order();

        if (data.discount_type === "percent") {
            order.add_global_discount(data.discount_value);
        } else {
            order.add_paymentline("Cash", -data.discount_value);
        }

        Gui.showPopup("ConfirmPopup", {
            title: "Descuento aplicado",
            body: "El código se aplicó correctamente.",
        });

        await _rpc({
            model: "pos.discount.code",
            method: "write",
            args: [[data.id], { used: true, fecha_uso: new Date() }],
        });
    }
}

DiscountCodeButton.template = "DiscountCodeButton";

registry.category("pos_buttons").add("DiscountCodeButton", DiscountCodeButton);
