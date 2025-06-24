/** @odoo-module */

import { usePos } from "@punto_de_venta/app/store/pos_hook";
import { ProductScreen } from "@punto_de_venta/app/screens/product_screen/product_screen";
import { Component } from "@odoo/owl";

export class CustomerButton extends Component {
    static template = "punto_de_venta.CustomerButton";

    setup() {
        this.pos = usePos();
    }

    get partner() {
        const order = this.pos.get_order();
        return order ? order.get_partner() : null;
    }
}

ProductScreen.addControlButton({
    component: CustomerButton,
    position: ["before", "SetFiscalPositionButton"],
    condition: function () {
        return this.pos.config.module_pos_restaurant;
    },
});
