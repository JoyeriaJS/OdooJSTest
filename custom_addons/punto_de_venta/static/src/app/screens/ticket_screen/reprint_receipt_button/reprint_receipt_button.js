/** @odoo-module */

import { usePos } from "@punto_de_venta/app/store/pos_hook";
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { OrderReceipt } from "@punto_de_venta/app/screens/receipt_screen/receipt/order_receipt";
import { useAsyncLockedMethod } from "@punto_de_venta/app/utils/hooks";

export class ReprintReceiptButton extends Component {
    static template = "punto_de_venta.ReprintReceiptButton";

    setup() {
        this.pos = usePos();
        this.printer = useService("printer");
        this.click = useAsyncLockedMethod(this.click);
    }

    async click() {
        if (!this.props.order) {
            return;
        }
        // Need to await to have the result in case of automatic skip screen.
        (await this.printer.print(OrderReceipt, {
            data: this.props.order.export_for_printing(),
            formatCurrency: this.env.utils.formatCurrency,
        })) || this.pos.showScreen("ReprintReceiptScreen", { order: this.props.order });
    }
}
