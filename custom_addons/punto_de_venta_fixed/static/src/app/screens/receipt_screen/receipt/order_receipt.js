/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Orderline } from "@punto_de_venta/app/generic_components/orderline/orderline";
import { OrderWidget } from "@punto_de_venta/app/generic_components/order_widget/order_widget";
import { ReceiptHeader } from "@punto_de_venta/app/screens/receipt_screen/receipt/receipt_header/receipt_header";
import { omit } from "@web/core/utils/objects";

export class OrderReceipt extends Component {
    static template = "punto_de_venta.OrderReceipt";
    static components = {
        Orderline,
        OrderWidget,
        ReceiptHeader,
    };
    static props = {
        data: Object,
        formatCurrency: Function,
    };
    omit(...args) {
        return omit(...args);
    }
}
