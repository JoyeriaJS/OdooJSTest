/** @odoo-module **/

import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { registry } from "@web/core/registry";
import { PosComponent } from "@point_of_sale/app/components/pos_component/pos_component";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class PosDiscountButton extends PosComponent {
    setup() {
        this.pos = usePos();
        console.log("🔥 Botón de Descuento CARGADO en ControlButtons");
    }

    onClick() {
        this.showPopup("ConfirmPopup", {
            title: "Descuento Autorizado",
            body: "El botón fue presionado correctamente."
        });
    }
}

PosDiscountButton.template = "PosDiscountButton";

registry.category("pos_control_buttons").add("PosDiscountButton", {
    component: PosDiscountButton,
    position: 6,  // lo inserta después de los otros botones
});
