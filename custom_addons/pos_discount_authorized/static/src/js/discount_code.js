
odoo.define('@pos_discount_authorized/js/discount_code', function (require) {
    "use strict";

    const { registry } = require("@web/core/registry");
    const { Gui } = require("@web/gui/gui");
    const rpc = require("@web/core/network/rpc_service");
    const { usePos } = require("@point_of_sale/app/store/pos_hook");
    const { Component } = owl;

    class DiscountButton extends Component {
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
            order.add_product(this.pos.db.get_product_by_id(this.pos.config.discount_product_id), {
                price: amount,
            });

            await rpc("/web/dataset/call_kw", {
                model: "pos.discount.code",
                method: "write",
                args: [[data.id], { used: true, fecha_uso: new Date() }],
            });

            Gui.showNotification("Descuento aplicado");
        }
    }

    DiscountButton.template = "DiscountButtonTemplate";

    registry.category("pos_ui").add("discount_button", DiscountButton);
});
