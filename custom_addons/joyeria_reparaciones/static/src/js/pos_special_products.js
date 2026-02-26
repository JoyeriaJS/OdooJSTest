/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Order, Orderline } from "@point_of_sale/app/store/models";
import { TextInputPopup } from "@point_of_sale/app/utils/input_popups/text_input_popup";
import { NumberPopup } from "@point_of_sale/app/utils/input_popups/number_popup";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { useService } from "@web/core/utils/hooks";

patch(Order.prototype, {

    async add_product(product, options = {}) {

        const popup = this.env.services.popup;

        // 🔵 PRODUCTO NO INVENTARIADO
        if (product.name === "Producto No Inventariado") {

            const gramos = await popup.add(NumberPopup, {
                title: "Ingrese gramos",
            });

            if (!gramos.confirmed || !gramos.payload) {
                await popup.add(ErrorPopup, {
                    title: "Dato obligatorio",
                    body: "Debe ingresar los gramos.",
                });
                return;
            }

            const precio = await popup.add(NumberPopup, {
                title: "Ingrese precio",
            });

            if (!precio.confirmed || !precio.payload) {
                await popup.add(ErrorPopup, {
                    title: "Dato obligatorio",
                    body: "Debe ingresar el precio.",
                });
                return;
            }

            const descripcion = await popup.add(TextInputPopup, {
                title: "Ingrese descripción",
            });

            if (!descripcion.confirmed || !descripcion.payload) {
                await popup.add(ErrorPopup, {
                    title: "Dato obligatorio",
                    body: "Debe ingresar la descripción.",
                });
                return;
            }

            options.price = parseFloat(precio.payload);

            await super.add_product(product, options);

            const line = this.get_selected_orderline();
            line.gramos = gramos.payload;
            line.descripcion_personalizada = descripcion.payload;

            return;
        }

        // 🔴 PRODUCTO RMA
        if (product.name === "Producto RMA") {

            const precio = await popup.add(NumberPopup, {
                title: "Ingrese precio RMA",
            });

            if (!precio.confirmed || !precio.payload) {
                await popup.add(ErrorPopup, {
                    title: "Dato obligatorio",
                    body: "Debe ingresar el precio.",
                });
                return;
            }

            options.price = parseFloat(precio.payload);

            await super.add_product(product, options);
            return;
        }

        return await super.add_product(product, options);
    },
});


// 🔥 EXTENDER ORDERLINE PARA GUARDAR DATOS

patch(Orderline.prototype, {

    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.gramos = this.gramos || "";
        json.descripcion_personalizada = this.descripcion_personalizada || "";
        return json;
    },

    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.gramos = json.gramos || "";
        this.descripcion_personalizada = json.descripcion_personalizada || "";
    },

    export_for_printing() {
        const line = super.export_for_printing(...arguments);
        line.gramos = this.gramos || "";
        line.descripcion_personalizada = this.descripcion_personalizada || "";
        return line;
    },

});