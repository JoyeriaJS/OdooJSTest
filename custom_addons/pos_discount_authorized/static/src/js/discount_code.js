/** @odoo-module **/

odoo.define('pos_discount_authorized.discount_button', function (require) {
    "use strict";

    const Chrome = require('point_of_sale.Chrome');
    const gui = require('point_of_sale.Gui');
    const rpc = require('web.rpc');

    Chrome.Chrome.include({

        async start() {
            await this._super(...arguments);

            this.addActionButton({
                name: 'discount_code',
                label: 'Código Descuento',
                icon: 'fa fa-tag',
                action: () => this.applyDiscountCode(),
            });
        },

        async applyDiscountCode() {
            const { confirmed, payload } = await gui.showPopup('TextInputPopup', {
                title: "Ingresar código de descuento",
            });

            if (!confirmed) return;

            const code = (payload || "").trim();

            const result = await rpc.query({
                model: "pos.discount.code",
                method: "search_read",
                args: [
                    [["code", "=", code]],
                    ["code", "discount_type", "discount_value", "used", "expired"]
                ],
            });

            if (!result || result.length === 0) {
                return gui.showPopup("ErrorPopup", {
                    title: "Código inválido",
                    body: "Este código no existe.",
                });
            }

            const data = result[0];

            if (data.used || data.expired) {
                return gui.showPopup("ErrorPopup", {
                    title: "No válido",
                    body: "El código está usado o expirado.",
                });
            }

            const order = this.env.pos.get_order();

            if (data.discount_type === "percent") {
                order.add_global_discount(data.discount_value);
            } else {
                order.add_paymentline(this.env.pos.cashregisters[0], -data.discount_value);
            }

            gui.showPopup("ConfirmPopup", {
                title: "Aplicado",
                body: "El descuento fue aplicado correctamente.",
            });

            await rpc.query({
                model: "pos.discount.code",
                method: "write",
                args: [[data.id], { used: true, fecha_uso: new Date() }],
            });
        },
    });
});
