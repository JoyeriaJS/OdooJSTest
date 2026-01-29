/** @odoo-module **/

import { PosComponent } from "@point_of_sale/app/components/base/pos_component";
import { registry } from "@web/core/registry";

export class PosDiscountButton extends PosComponent {
    setup() {
        super.setup();
        console.log("🔥 Botón de Descuento CARGADO correctamente en Odoo 17 Community");
    }

    onClick() {
        alert("Botón funcionando!");
    }
}

PosDiscountButton.template = "PosDiscountButton";

registry.category("pos_screens").add("PosDiscountButton", {
    component: PosDiscountButton,
    position: ["product-buttons"],  // ← aparecerá en la zona correcta
});
