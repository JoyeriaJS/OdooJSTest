odoo.define('pos_discount_authorized', function (require) {
    "use strict";

    const ProductScreen = require('point_of_sale.ProductScreen');
    const { Gui } = require('point_of_sale.Gui');
    const rpc = require('web.rpc');

    ProductScreen.include({

        async authorizeDiscount() {

            const { confirmed, payload } = await Gui.prompt({
                title: "Descuento autorizado",
                body: "Ingrese el código entregado por el administrador.",
                inputType: "text",
            });

            if (!confirmed) return;

            const code = payload.trim().toUpperCase();

            const validation = await rpc.query({
                model: "pos.authorized.discount",
                method: "validate_code",
                args: [code],
            });

            if (!validation.ok) {
                return Gui.showPopup("ErrorPopup", {
                    title: "Código inválido",
                    body: validation.error,
                });
            }

            // Obtener línea actual o aplicar al pedido completo
            const order = this.env.pos.get_order();

            if (validation.type === "percent") {
                order.add_global_discount(validation.value);
            } else if (validation.type === "amount") {
                order.add_product(this.env.pos.db.product_by_id[1], {
                    price: -validation.value,
                });
            }

            Gui.showPopup("ConfirmPopup", {
                title: "Descuento aplicado",
                body: `Se aplicó el descuento: ${validation.value} (${validation.type})`,
            });
        },

        // Agregar botón al POS
        get buttons() {
            const buttons = super.buttons;
            buttons.push({
                name: "authorized_discount_button",
                label: "Descuento Autorizado",
                class: "btn btn-primary",
                command: "authorizeDiscount",
            });
            return buttons;
        },
    });
});
