/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { TextInputPopup } from "@point_of_sale/app/utils/input_popups/text_input_popup";
import { NumberPopup } from "@point_of_sale/app/utils/input_popups/number_popup";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { Orderline } from "@point_of_sale/app/store/models";

patch(ProductScreen.prototype, {

    async addProductToCurrentOrder(product, options = {}) {

        // 🔵 PRODUCTO NO INVENTARIADO
        if (product.display_name === "Producto No Inventariado") {

            const gramos = await this.popup.add(NumberPopup, {
                title: "Ingrese gramos",
            });

            if (!gramos.confirmed || !gramos.payload) {
                await this.popup.add(ErrorPopup, {
                    title: "Dato obligatorio",
                    body: "Debe ingresar los gramos.",
                });
                return;
            }

            const precio = await this.popup.add(NumberPopup, {
                title: "Ingrese precio",
            });

            if (!precio.confirmed || !precio.payload) {
                await this.popup.add(ErrorPopup, {
                    title: "Dato obligatorio",
                    body: "Debe ingresar el precio.",
                });
                return;
            }

            const descripcion = await this.popup.add(TextInputPopup, {
                title: "Ingrese descripción",
            });

            if (!descripcion.confirmed || !descripcion.payload) {
                await this.popup.add(ErrorPopup, {
                    title: "Dato obligatorio",
                    body: "Debe ingresar la descripción.",
                });
                return;
            }

            const order = this.currentOrder;

            order.add_product(product, {
                price: parseFloat(precio.payload),
            });

            const line = order.get_selected_orderline();
            line.gramos = gramos.payload;
            line.descripcion_personalizada = descripcion.payload;

            return;
        }

        // 🔴 PRODUCTO RMA
        if (product.display_name === "Producto RMA") {

            const precio = await this.popup.add(NumberPopup, {
                title: "Ingrese precio RMA",
            });

            if (!precio.confirmed || !precio.payload) {
                await this.popup.add(ErrorPopup, {
                    title: "Dato obligatorio",
                    body: "Debe ingresar el precio.",
                });
                return;
            }

            const order = this.currentOrder;

            order.add_product(product, {
                price: parseFloat(precio.payload),
            });

            return;
        }

        return super.addProductToCurrentOrder(product, options);
    },
});


/* 🔥 EXTENSIÓN DE ORDERLINE PARA GUARDAR DATOS */

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

});