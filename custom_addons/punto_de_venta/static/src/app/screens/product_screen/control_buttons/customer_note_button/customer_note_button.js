/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { ProductScreen } from "@punto_de_venta/app/screens/product_screen/product_screen";
import { useService } from "@web/core/utils/hooks";
import { TextAreaPopup } from "@punto_de_venta/app/utils/input_popups/textarea_popup";
import { Component } from "@odoo/owl";
import { usePos } from "@punto_de_venta/app/store/pos_hook";

export class OrderlineCustomerNoteButton extends Component {
    static template = "punto_de_venta.OrderlineCustomerNoteButton";

    setup() {
        this.pos = usePos();
        this.popup = useService("popup");
    }
    async onClick() {
        const selectedOrderline = this.pos.get_order().get_selected_orderline();
        // FIXME POSREF can this happen? Shouldn't the orderline just be a prop?
        if (!selectedOrderline) {
            return;
        }
        const { confirmed, payload: inputNote } = await this.popup.add(TextAreaPopup, {
            startingValue: selectedOrderline.get_customer_note(),
            title: _t("Add Customer Note"),
        });

        if (confirmed) {
            selectedOrderline.set_customer_note(inputNote);
        }
    }
}

ProductScreen.addControlButton({
    component: OrderlineCustomerNoteButton,
});
