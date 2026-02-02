/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { useService } from "@web/core/utils/hooks";

patch(ProductScreen.prototype, {
    setup() {
        super.setup();
        this.popup = useService("popup");
        console.log("🔥 BOTÓN DE DESCUENTO ACTIVADO EN ODOO 17 COMMUNITY");
    },

    async onClickDiscount() {
        const result = await this.popup.add({
            type: "text",
            title: "Código de autorización",
            body: "Ingresa el código para aplicar descuento",
        });

        if (result && result.confirmed) {
            const code = result.payload;

            if (code === "1234") {
                alert("Código correcto. Puedes aplicar el descuento.");
            } else {
                alert("Código incorrecto.");
            }
        }
    },
});
