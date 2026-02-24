/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { Order } from "@point_of_sale/app/store/models";
import { TextInputPopup } from "@point_of_sale/app/utils/input_popups/text_input_popup";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";


// 🔹 PEDIR QR SIEMPRE
patch(PaymentScreen.prototype, {

    async validateOrder(isForceValidate) {

        const order = this.currentOrder;

        if (!this.pos.vendedoras || !this.pos.vendedoras.length) {
            await this.popup.add(ErrorPopup, {
                title: "Error",
                body: "No hay vendedoras cargadas en el POS.",
            });
            return;
        }

        const { confirmed, payload } = await this.popup.add(TextInputPopup, {
            title: "Escanear QR de Vendedora",
            body: "Ingrese o escanee el código.",
        });

        if (!confirmed) {
            return;
        }

        const codigo = (payload || "").trim().toLowerCase();

        if (!codigo) {
            await this.popup.add(ErrorPopup, {
                title: "Código requerido",
                body: "Debe ingresar un código válido.",
            });
            return;
        }

        const vendedora = this.pos.vendedoras.find(v =>
            String(v.codigo_qr || "")
                .trim()
                .toLowerCase() === codigo
        );

        if (!vendedora) {
            await this.popup.add(ErrorPopup, {
                title: "Código inválido",
                body: "No existe una vendedora con ese código.",
            });
            return;
        }

        order.vendedora_id = vendedora.id;
        order.vendedora_name = vendedora.name;

        return super.validateOrder(isForceValidate);
    },
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