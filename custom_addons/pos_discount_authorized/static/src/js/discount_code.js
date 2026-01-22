/** @odoo-module **/

import { PosComponent } from "@point_of_sale/app/components/pos_component/pos_component";
import { registry } from "@web/core/registry";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Gui } from "@web/gui/gui";
import { onMounted } from "@odoo/owl";
import { _rpc } from "@web/core/network/rpc_service";

export class DiscountCodeButton extends PosComponent {
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

        let codigo = popup.payload.trim();

        // Buscar código en Odoo
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
                body: "No existe el código.",
            });
            return;
        }

        let data = result[0];

        if (data.used || data.expired) {
            Gui.showPopup("ErrorPopup", {
                title: "Código inválido",
                body: "Código usado o expirado.",
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
            body: "Código aplicado correctamente.",
        });

        // Marcar como usado
        await _rpc({
            model: "pos.discount.code",
            method: "write",
            args: [[data.id], { used: true, fecha_uso: new Date() }],
        });
    }
}

DiscountCodeButton.template = "DiscountCodeButton";

registry.category("pos_buttons").add("DiscountCodeButton", DiscountCodeButton);
