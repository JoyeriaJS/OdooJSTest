odoo.define('pos_discount_authorized.discount_button', function (require) {
    'use strict';

    const rpc = require('web.rpc');
    const core = require('web.core');
    const screens = require('point_of_sale.screens');

    const _t = core._t;

    screens.ActionpadWidget.include({

        renderElement: function () {
            this._super();
            const self = this;

            // Click al botón de código autorizado
            this.$el.find('.button.btn.btn-primary').click(async function () {

                const code = prompt("Ingrese código autorizado:");

                if (!code) return;

                // Buscar el código en el modelo
                const result = await rpc.query({
                    model: "pos.discount.code",
                    method: "search_read",
                    args: [[["code", "=", code.toUpperCase()]],
                           ["discount_type", "discount_value", "used", "expired"]],
                });

                if (!result.length) {
                    alert("Código inválido.");
                    return;
                }

                const data = result[0];

                if (data.used || data.expired) {
                    alert("Código ya usado o expirado.");
                    return;
                }

                // Aplicar el descuento
                const order = self.pos.get_order();
                const total = order.get_total_with_tax();

                let amount = 0;

                if (data.discount_type === "percent") {
                    amount = -(total * (data.discount_value / 100));
                } else {
                    amount = -data.discount_value;
                }

                order.add_product(
                    self.pos.db.get_product_by_id(self.pos.config.discount_product_id),
                    { price: amount }
                );

                // Marcar como usado
                await rpc.query({
                    model: "pos.discount.code",
                    method: "write",
                    args: [[data.id], { used: true }],
                });

                alert("Descuento aplicado correctamente.");
            });
        }

    });

});
