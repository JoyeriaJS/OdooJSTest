/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { Order } from "@point_of_sale/app/store/models";
import { TextInputPopup } from "@point_of_sale/app/utils/input_popups/text_input_popup";
import { PosGlobalState } from "@point_of_sale/app/store/pos_global_state";
import { registry } from "@web/core/registry";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";


// ======================================================
// 🔹 1️⃣ CARGAR MODELO joyeria.vendedora EN EL POS
// ======================================================

registry.category("pos_models").add("joyeria_vendedora", {
    model: "joyeria.vendedora",
    fields: ["name", "codigo_qr", "clave_qr", "clave_autenticacion"],
    loaded: function (self, vendedoras) {
        self.vendedoras = vendedoras;
    },
});

patch(PosGlobalState.prototype, {
    async _processData(loadedData) {
        await super._processData(...arguments);
        this.vendedoras = loadedData["joyeria.vendedora"] || [];
    },
});


// ======================================================
// 🔹 2️⃣ PEDIR QR ANTES DE VALIDAR
// ======================================================

patch(PaymentScreen.prototype, {

    async validateOrder(isForceValidate) {

        const order = this.currentOrder;

        const { confirmed, payload } = await this.popup.add(TextInputPopup, {
            title: "Escanear QR de Vendedora",
            body: "Debe escanear o ingresar el código antes de validar la venta.",
        });

        if (!confirmed) {
            return;
        }

        const codigo = (payload || "").trim().toUpperCase();

        if (!codigo) {
            await this.popup.add(ErrorPopup, {
                title: "Código requerido",
                body: "Debe ingresar un código válido.",
            });
            return;
        }

        const vendedora = this.pos.vendedoras?.find(v =>
            (v.codigo_qr && v.codigo_qr.toUpperCase() === codigo) ||
            (v.clave_qr && v.clave_qr.toUpperCase() === codigo) ||
            (v.clave_autenticacion && v.clave_autenticacion.toUpperCase() === codigo)
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
        order.codigo_qr_vendedora = codigo;

        await super.validateOrder(...arguments);
    },
});


// ======================================================
// 🔹 3️⃣ EXTENDER ORDER
// ======================================================

patch(Order.prototype, {

    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.vendedora_id = this.vendedora_id || false;
        json.codigo_qr_vendedora = this.codigo_qr_vendedora || false;
        return json;
    },

    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.vendedora_id = json.vendedora_id || false;
        this.codigo_qr_vendedora = json.codigo_qr_vendedora || false;
        this.vendedora_name = json.vendedora_name || false;
    },

    export_for_printing() {
        const result = super.export_for_printing(...arguments);

        result.vendedora_name = this.vendedora_name || null;

        return result;
    },
});