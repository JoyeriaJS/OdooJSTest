/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { rpc } from "@web/core/network/rpc";

patch(PaymentScreen.prototype, {

    async validateOrder(isForceValidate) {

        const order = this.currentOrder;

        let valid = false;
        let codigo = false;

        while (!valid) {

            const { confirmed, payload } = await this.showPopup('TextInputPopup', {
                title: 'Escanear QR de Vendedora',
                body: 'Debe escanear el código QR antes de validar.',
            });

            if (!confirmed || !payload) {
                return;
            }

            codigo = payload.trim();

            // 🔎 Validamos contra backend antes de guardar
            const result = await rpc('/web/dataset/call_kw', {
                model: 'joyeria.vendedora',
                method: 'search_read',
                args: [[['codigo_qr', '=', codigo]], ['id']],
                kwargs: { limit: 1 }
            });

            if (result.length > 0) {
                valid = true;
            } else {
                await this.showPopup('ErrorPopup', {
                    title: 'QR inválido',
                    body: 'El código escaneado no corresponde a ninguna vendedora.'
                });
            }
        }

        // Solo si es válido se guarda
        order.codigo_qr_vendedora = codigo;

        await super.validateOrder(isForceValidate);
    }
});