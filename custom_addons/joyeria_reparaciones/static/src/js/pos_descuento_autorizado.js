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

        // ==============================
        // VALIDACIÓN 50% PRECIO MÍNIMO
        // ==============================

        const lines = order.get_orderlines();

        for (let line of lines) {

            const precioOriginal = line.product.lst_price;
            const precioVenta = line.get_unit_price();

            if (precioVenta < (precioOriginal * 0.5)) {

                alert(
                    "No se puede vender el producto '" +
                    line.product.display_name +
                    "' por menos del 50% de su precio original."
                );

                return;
            }
        }


        // ==============================
        // DESCUENTO AUTORIZADO
        // ==============================

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

                if (descuento) {

                    let total = order.get_total_with_tax();

                    if (descuento.tipo_descuento === "porcentaje") {

                        total = total - (total * (parseFloat(descuento.porcentaje) / 100));

                    }

                    if (descuento.tipo_descuento === "monto") {

                        total = total - descuento.monto;

                    }

                    total = Math.round(total);

                    alert("Descuento aplicado correctamente");

                } else {

                    alert("Código inválido o ya utilizado");
                    return;

                }

            }

        }

        await super.validateOrder(isForceValidate);
    }

});