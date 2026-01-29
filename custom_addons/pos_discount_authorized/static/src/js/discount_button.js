/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";

patch(ProductScreen.prototype, "discount_button_patch", {
    setup() {
        super.setup();
        console.log("BOTÓN DE DESCUENTO INYECTADO (COMMUNITY MODE)");
    },

    // Este método se llamará al presionar el botón
    onClickDiscount() {
        alert("Descuento funcionando desde Community!");
    },
});
