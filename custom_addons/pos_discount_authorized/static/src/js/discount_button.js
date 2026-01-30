/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";

patch(ProductScreen.prototype, {
    setup() {
        super.setup();
        console.log("🔥 DESCUENTO EN PRODUCT SCREEN CARGADO ✔");
    },

    onClickDiscount() {
        alert("Descuento funcionando en Community!");
    },
});
