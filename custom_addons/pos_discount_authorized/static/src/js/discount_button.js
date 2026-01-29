/** @odoo-module **/

import { registry } from "@web/core/registry";
import { PosComponent } from "@point_of_sale/app/components/pos_component/pos_component";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class PosDiscountButton extends PosComponent {
    setup() {
        this.pos = usePos();
        console.log("🔥 POS DISCOUNT MODULE LOADED CORRECTLY 🔥");
    }

    onClick() {
        alert("Botón de descuento funcionando!");
    }
}

PosDiscountButton.template = "PosDiscountButton";

registry.category("pos_screens").add("PosDiscountButton", {
    component: PosDiscountButton,
    position: ["actionpad-buttons"],  // ← lo verás de inmediato
});
