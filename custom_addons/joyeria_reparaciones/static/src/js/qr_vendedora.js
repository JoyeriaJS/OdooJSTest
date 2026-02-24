/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { Order } from "@point_of_sale/app/store/models";
import { TextInputPopup } from "@point_of_sale/app/utils/input_popups/text_input_popup";
import { PosStore } from "@point_of_sale/app/store/pos_store";


// 🔹 CARGAR VENDEDORAS EN EL POS
patch(PosStore.prototype, {

    async _processData(loadedData) {
        await super._processData(...arguments);

        // Guardamos las vendedoras en memoria del POS
        this.vendedoras = loadedData['joyeria.vendedora'] || [];
    },

});


// 🔹 PEDIR QR SIEMPRE ANTES DE VALIDAR
patch(PaymentScreen.prototype, {

    async validateOrder(isForceValidate) {

        const order = this.currentOrder;

        // Verificar que el modelo esté cargado
        if (!this.pos || !this.pos.vendedoras) {
            console.error("No se cargaron las vendedoras en el POS");
            return;
        }

        const { confirmed, payload } = await this.popup.add(TextInputPopup, {
            title: "Escanear QR de Vendedora",
            body: "Debe escanear o ingresar el código antes de validar la venta.",
        });

        if (!confirmed || !payload) {
            return;
        }

        const codigo = payload.trim();

        // Buscar vendedora
        const vendedora = this.pos.vendedoras.find(
            v => v.codigo_qr === codigo
        );

        if (!vendedora) {
            await this.popup.add(TextInputPopup, {
                title: "Código inválido",
                body: "No existe una vendedora con ese QR.",
            });
            return;
        }

        // Guardamos datos en la orden
        order.vendedora_id = vendedora.id;
        order.vendedora_name = vendedora.name;

        await super.validateOrder(...arguments);
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