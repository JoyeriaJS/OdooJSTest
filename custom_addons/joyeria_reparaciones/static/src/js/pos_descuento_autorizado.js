/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { useService } from "@web/core/utils/hooks";

patch(PaymentScreen.prototype, {

    setup() {
        super.setup();
        this.rpc = useService("rpc");
    },

    async validateOrder(isForceValidate) {

        const order = this.currentOrder;
        const paymentlines = order.paymentlines;

        let metodoPermitido = false;

        paymentlines.forEach(line => {

            const name = line.payment_method.name.toLowerCase();

            if (name.includes("efectivo") || name.includes("transferencia")) {
                metodoPermitido = true;
            }

        });

        if (metodoPermitido) {

            const codigo = prompt("Ingrese código de autorización de descuento");

            if (codigo) {

                const descuento = await this.rpc("/pos/validar_descuento", {
                    codigo: codigo
                });

                if (!descuento) {
                    alert("Código inválido o ya usado");
                    return;
                }

                let porcentaje = 0;

                if (descuento.tipo_descuento === "porcentaje") {
                    porcentaje = parseFloat(descuento.porcentaje);
                }

                if (descuento.tipo_descuento === "monto") {

                    const total = order.get_total_with_tax();

                    porcentaje = (descuento.monto / total) * 100;

                }

                porcentaje = Math.round(porcentaje);

                order.get_orderlines().forEach(line => {
                    line.set_discount(porcentaje);
                });

            }

        }

        await super.validateOrder(...arguments);
    }

});