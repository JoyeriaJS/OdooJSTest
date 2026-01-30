/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { PosComponent } from "@point_of_sale/app/components/pos_component/pos_component";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class PosDiscountButton extends PosComponent {
    setup() {
        this.pos = usePos();
        console.log("🔥 BOTÓN DE DESCUENTO INYECTADO EN COMMUNITY 🔥");
    }

    onClick() {
        alert("Descuento autorizado funcionando!");
    }
}

PosDiscountButton.template = "PosDiscountButton";

// INYECCIÓN CORRECTA PARA ODOO COMMUNITY
ProductScreen.addControlButton({
    component: PosDiscountButton,
    condition: () => true,  // siempre visible
    position: ["before", "set-customer"], // posición en la barra inferior
});
