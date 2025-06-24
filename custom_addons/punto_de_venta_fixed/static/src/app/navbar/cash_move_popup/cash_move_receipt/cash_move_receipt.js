/** @odoo-module **/

import { Component } from "@odoo/owl";
import { ReceiptHeader } from "@punto_de_venta/app/screens/receipt_screen/receipt/receipt_header/receipt_header";

export class CashMoveReceipt extends Component {
    static template = "punto_de_venta.CashMoveReceipt";
    static components = { ReceiptHeader };
    static props = {
        reason: String,
        translatedType: String,
        formattedAmount: String,
        headerData: Object,
        date: String,
    };
}
