/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { useService } from "@web/core/utils/hooks";

patch(PaymentScreen.prototype, {

    async validateOrder(isForceValidate) {

        const order = this.currentOrder;

        if (!order.codigo_qr_vendedora) {

            const { confirmed, payload } = await this.showPopup('TextInputPopup', {
                title: 'Escanear QR de Vendedora',
                body: 'Debe escanear el código QR antes de validar.',
            });

            if (!confirmed || !payload) {
                return;
            }

            order.codigo_qr_vendedora = payload;
        }

        await super.validateOrder(isForceValidate);
    }
});

import { Order } from "@point_of_sale/app/store/models";

patch(Order.prototype, {

    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.codigo_qr_vendedora = this.codigo_qr_vendedora || false;
        return json;
    },

    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.codigo_qr_vendedora = json.codigo_qr_vendedora;
    },
});