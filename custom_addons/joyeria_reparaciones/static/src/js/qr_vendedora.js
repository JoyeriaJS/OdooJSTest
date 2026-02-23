/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { Order } from "@point_of_sale/app/store/models";
import { TextInputPopup } from "@point_of_sale/app/utils/input_popups/text_input_popup";


// 🔹 PEDIR QR SIEMPRE
patch(PaymentScreen.prototype, {

    async validateOrder(isForceValidate) {

        const order = this.currentOrder;

        const { confirmed, payload } = await this.popup.add(TextInputPopup, {
            title: "Escanear QR de Vendedora",
            body: "Debe escanear el código QR antes de validar la venta.",
        });

        if (!confirmed || !payload) {
            return;
        }

        // Guardamos el código escaneado
        order.codigo_qr_vendedora = payload.trim();

        await super.validateOrder(...arguments);
    },
});


// 🔹 HACER QUE EL RECIBO RECIBA LA VENDEDORA
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

    // 👇 ESTE ES EL MÉTODO QUE FALTABA
    export_for_printing() {
        const result = super.export_for_printing(...arguments);

        // Pasamos la vendedora al receipt
        result.vendedora_name = this.codigo_qr_vendedora || null;

        return result;
    },

});