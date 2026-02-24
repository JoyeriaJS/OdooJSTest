/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { Order } from "@point_of_sale/app/store/models";
import { TextInputPopup } from "@point_of_sale/app/utils/input_popups/text_input_popup";


/* ============================================================
   🔹 VALIDAR QR ANTES DE CONFIRMAR LA VENTA
============================================================ */
patch(PaymentScreen.prototype, {

    async validateOrder(isForceValidate) {

        const order = this.currentOrder;

        // 🔹 Verificar que existan vendedoras cargadas
        if (!this.pos.vendedoras || this.pos.vendedoras.length === 0) {
            console.error("No hay vendedoras cargadas en el POS");
            await this.popup.add(TextInputPopup, {
                title: "Error",
                body: "No hay vendedoras cargadas en el sistema.",
            });
            return;
        }

        // 🔹 Pedir QR
        const { confirmed, payload } = await this.popup.add(TextInputPopup, {
            title: "Escanear QR de Vendedora",
            body: "Debe escanear o ingresar el código antes de validar.",
        });

        if (!confirmed || !payload) {
            return;
        }

        const codigoIngresado = String(payload).trim().toLowerCase();

        // 🔹 Buscar vendedora de forma segura
        const vendedora = this.pos.vendedoras.find(v =>
            String(v.codigo_qr || "")
                .trim()
                .toLowerCase() === codigoIngresado
        );

        if (!vendedora) {
            await this.popup.add(TextInputPopup, {
                title: "Código inválido",
                body: "No existe una vendedora con ese código.",
            });
            return;
        }

        // 🔹 Guardar en la orden
        order.vendedora_id = vendedora.id;
        order.vendedora_name = vendedora.name;

        console.log("Vendedora asignada:", vendedora.name);

        await super.validateOrder(...arguments);
    },
});


/* ============================================================
   🔹 EXTENDER ORDER PARA GUARDAR DATOS
============================================================ */
patch(Order.prototype, {

    setup() {
        super.setup(...arguments);
        this.vendedora_id = this.vendedora_id || false;
        this.vendedora_name = this.vendedora_name || false;
    },

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
        result.vendedora_name = this.vendedora_name || "";
        return result;
    },
});

patch(PosStore.prototype, {
    async _processData(loadedData) {
        await super._processData(...arguments);
        this.vendedoras = loadedData["joyeria.vendedora"];
    },
});