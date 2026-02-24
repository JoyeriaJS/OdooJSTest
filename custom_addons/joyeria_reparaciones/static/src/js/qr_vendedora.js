/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { Order } from "@point_of_sale/app/store/models";
import { TextInputPopup } from "@point_of_sale/app/utils/input_popups/text_input_popup";


// 🔹 PEDIR QR SIEMPRE
patch(PaymentScreen.prototype, {

    async validateOrder(isForceValidate) {

        const popup = this.popup;

        const { confirmed, payload } = await popup.add(this.env.services.popup.constructor, {
            title: "Código de Vendedora",
            body: "Ingrese el código de la vendedora",
        });

        if (!confirmed || !payload) {
            return;
        }

        const codigoIngresado = payload.trim();

        // 🔥 AQUÍ ESTÁ LA CLAVE
        const usuarios = this.env.pos.users || [];

        const vendedora = usuarios.find(user =>
            user.codigo_vendedora === codigoIngresado
        );

        if (!vendedora) {
            await popup.add(this.env.services.popup.constructor, {
                title: "Error",
                body: "Debe escanear o ingresar el código de la vendedora.",
            });
            return;
        }

        // Guardamos la vendedora en la orden
        this.currentOrder.codigo_vendedora = codigoIngresado;

        return super.validateOrder(isForceValidate);
    }

});


// 🔹 EXTENDER ORDER
patch(Order.prototype, {

    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.vendedora_id = this.vendedora_id || false;
        json.vendedora_name = this.vendedora_name || false;
        return json;
    },

    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.vendedora_id = json.vendedora_id || false;
        this.vendedora_name = json.vendedora_name || false;
    },

    export_for_printing() {
        const result = super.export_for_printing(...arguments);

        result.vendedora_name = this.vendedora_name || null;

        return result;
    },
});