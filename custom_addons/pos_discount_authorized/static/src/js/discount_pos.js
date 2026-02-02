odoo.define('pos_discount_authorized.discount_pos', function(require) {
    'use strict';

    const { registry } = require("@web/core/registry");
    const { useState } = owl;
    const PosComponent = require('point_of_sale.PosComponent');
    const DiscountButton = require('point_of_sale.DiscountButton');
    const { Gui } = require('point_of_sale.Gui');
    const rpc = require('web.rpc');

    class AuthorizedDiscountPopup extends PosComponent {
        setup() {
            this.state = useState({ code: "" });
        }

        cancel() {
            this.trigger('close');
        }

        async confirm() {
            const code = this.state.code.trim();
            if (!code) {
                Gui.showPopup("ErrorPopup", {
                    title: "Error",
                    body: "Debe ingresar un código"
                });
                return;
            }

            const result = await rpc.query({
                model: "pos.authorized.discount",
                method: "search_read",
                args: [[["code", "=", code]], ["id", "discount_type", "value", "used", "expires_at"]],
            });

            if (!result.length) {
                Gui.showPopup("ErrorPopup", { title: "Código inválido", body: "No existe." });
                return;
            }

            const record = result[0];

            if (record.used) {
                Gui.showPopup("ErrorPopup", { title: "Error", body: "Código ya utilizado" });
                return;
            }

            Gui.showPopup("NumberPopup", {
                title: "Descuento autorizado",
                startingValue: record.value,
                confirm: (val) => {
                    this.env.pos.get_order().add_discount(val);
                }
            });

            await rpc.query({
                model: "pos.authorized.discount",
                method: "write",
                args: [[record.id], { used: true }]
            });

            this.trigger('close');
        }
    }

    AuthorizedDiscountPopup.template = "PosDiscountAuthorizationPopup";
    registry.category("popups").add("PosDiscountAuthorizationPopup", AuthorizedDiscountPopup);

    class AuthorizedDiscountButton extends DiscountButton {
        async onClick() {
            Gui.showPopup("PosDiscountAuthorizationPopup");
        }
    }

    AuthorizedDiscountButton.template = "DiscountButton";
    registry.category("pos_buttons").add("AuthorizedDiscountButton", AuthorizedDiscountButton);
});
