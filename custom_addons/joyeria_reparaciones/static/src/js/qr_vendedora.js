/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { Order } from "@point_of_sale/app/store/models";
import { TextInputPopup } from "@point_of_sale/app/utils/input_popups/text_input_popup";

patch(PaymentScreen.prototype, {

    async validateOrder(isForceValidate) {

        const order = this.currentOrder;

        // 🔥 SIEMPRE pedir QR
        const { confirmed, payload } = await this.popup.add(TextInputPopup, {
            title: "Escanear QR de Vendedora",
            body: "Debe escanear el código QR antes de validar la venta.",
        });

        if (!confirmed || !payload) {
            return;
        }

        // 🔁 Siempre reemplazamos
        order.codigo_qr_vendedora = payload.trim();

        await super.validateOrder(...arguments);
    },
});


patch(Order.prototype, {

    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.codigo_qr_vendedora = this.codigo_qr_vendedora || false;
        return json;
    },

    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.codigo_qr_vendedora = json.codigo_qr_vendedora || false;
    },

    // 🔥 Para el recibo
    get_vendedora_name() {
        return this.codigo_qr_vendedora || "";
    }
});