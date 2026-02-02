odoo.define("pos_discount_authorized.discount_pos", function (require) {
    "use strict";

    const NumberBuffer = require("point_of_sale.NumberBuffer");
    const Registries = require("point_of_sale.Registries");
    const DiscountButton = require("point_of_sale.DiscountButton");
    const { useListener } = require("web.custom_hooks");

    const rpc = require("web.rpc");

    const AuthorizedDiscountButton = (DiscountButton) =>
        class extends DiscountButton {
            setup() {
                super.setup();
                useListener("click", this.onClick);
            }

            async onClick() {
                const { confirmed, payload } = await this.showPopup("TextInputPopup", {
                    title: "Código de autorización",
                    placeholder: "Ingrese el código autorizado…",
                });

                if (!confirmed || !payload) return;

                const code = payload.trim().toUpperCase();

                const result = await rpc.query({
                    model: "pos.authorized.discount",
                    method: "validate_code",
                    args: [code],
                });

                if (!result.ok) {
                    return this.showPopup("ErrorPopup", {
                        title: "Código inválido",
                        body: result.error,
                    });
                }

                const order = this.env.pos.get_order();
                const discType = result.type;
                const value = result.value;

                if (discType === "percent") {
                    order.set_discount(value);
                } else {
                    order.set_discount_fixed(value);
                }

                this.showPopup("ConfirmPopup", {
                    title: "Descuento aplicado",
                    body: "Código validado correctamente.",
                });
            }
        };

    Registries.Component.extend(DiscountButton, AuthorizedDiscountButton);

    return AuthorizedDiscountButton;
});
