/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
patch(ActionPad.prototype, {
    setup() {
        super.setup();
        console.log("🔥 Botón de descuento cargado en ActionPad (v17 Community) 🔥");
    },

    onClickDiscount() {
        alert("Descuento funcionando en Community!");
    },
});
