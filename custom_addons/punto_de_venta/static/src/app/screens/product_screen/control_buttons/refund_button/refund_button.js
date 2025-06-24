/** @odoo-module */

import { usePos } from "@punto_de_venta/app/store/pos_hook";
import { ProductScreen } from "@punto_de_venta/app/screens/product_screen/product_screen";
import { Component } from "@odoo/owl";

export class RefundButton extends Component {
    static template = "punto_de_venta.RefundButton";

    setup() {
        this.pos = usePos();
    }
    click() {
        const order = this.pos.get_order();
        const partner = order.get_partner();
        const searchDetails = partner ? { fieldName: "PARTNER", searchTerm: partner.name } : {};
        this.pos.showScreen("TicketScreen", {
            ui: { filter: "SYNCED", searchDetails },
            destinationOrder: order,
        });
    }
}

ProductScreen.addControlButton({
    component: RefundButton,
    condition: function () {
        return true;
    },
});
