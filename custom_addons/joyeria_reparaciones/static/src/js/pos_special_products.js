/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { TextInputPopup } from "@point_of_sale/app/utils/input_popups/text_input_popup";
import { NumberPopup } from "@point_of_sale/app/utils/input_popups/number_popup";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

patch(ProductScreen.prototype, {

    async _onClickProduct(event) {
        const product = event.detail;

        // 🔵 PRODUCTO NO INVENTARIADO
        if (product.name === "Producto No Inventariado") {

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
        if (product.name === "Producto RMA") {

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

        return super._onClickProduct(event);
    },
});