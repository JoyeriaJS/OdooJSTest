/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Order, Orderline } from "@point_of_sale/app/store/models";
import { TextInputPopup } from "@point_of_sale/app/utils/input_popups/text_input_popup";
import { NumberPopup } from "@point_of_sale/app/utils/input_popups/number_popup";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

patch(Order.prototype, {

    async add_product(product, options = {}) {

        const popup = this.env.services.popup;
        const rpc = this.env.services.rpc;

        // ===================================
        // PRODUCTO NO INVENTARIADO
        // ===================================

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

        // ===================================
        // PRODUCTO RMA
        // ===================================

        if (product.name === "Producto RMA") {

            const rmaInput = await popup.add(TextInputPopup, {
                title: "Ingrese número de RMA",
                placeholder: "Ej: RMA/01160 o 1160"
            });

            if (!rmaInput.confirmed || !rmaInput.payload) {
                await popup.add(ErrorPopup, {
                    title: "Dato obligatorio",
                    body: "Debe ingresar el número de RMA.",
                });
                return;
            }

            const numeroRMA = rmaInput.payload;

            // 🔵 CONSULTAR BACKEND
            const resultado = await rpc('/pos/buscar_rma', {
                numero_rma: numeroRMA
            });

            if (resultado.error) {

                await popup.add(ErrorPopup, {
                    title: "Error",
                    body: resultado.error,
                });

                return;
            }

            // 🔵 USAR PRECIO DEL ABONO
            options.price = parseFloat(resultado.precio);

            await super.add_product(product, options);

            const line = this.get_selected_orderline();
            line.numero_rma = resultado.rma;

            return;
        }

        return await super.add_product(product, options);
    },
});


// ===================================
// EXTENDER ORDERLINE
// ===================================

patch(Orderline.prototype, {

    export_as_JSON() {

        const json = super.export_as_JSON(...arguments);

        json.gramos = this.gramos || "";
        json.descripcion_personalizada = this.descripcion_personalizada || "";
        json.numero_rma = this.numero_rma || "";

        return json;
    },

    init_from_JSON(json) {

        super.init_from_JSON(...arguments);

        this.gramos = json.gramos || "";
        this.descripcion_personalizada = json.descripcion_personalizada || "";
        this.numero_rma = json.numero_rma || "";
    },

    export_for_printing() {

        const line = super.export_for_printing(...arguments);

        line.gramos = this.gramos || "";
        line.descripcion_personalizada = this.descripcion_personalizada || "";
        line.numero_rma = this.numero_rma || "";

        return line;
    },

});