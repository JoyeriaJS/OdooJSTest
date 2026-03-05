/** @odoo-module **/

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

patch(PaymentScreen.prototype, {

    setup() {
        super.setup();
        this.orm = useService("orm");
    },

    async addNewPaymentLine(paymentMethod) {

        await super.addNewPaymentLine(paymentMethod);

        const metodo = paymentMethod.name.toLowerCase();

        if (metodo === "efectivo" || metodo === "transferencia") {

            const codigo = prompt("Ingrese código de autorización de descuento");

            if (!codigo) {
                return;
            }

            try {

                const descuento = await this.orm.call(
                    "pos.descuento.autorizado",
                    "validar_codigo_pos",
                    [codigo]
                );

                if (!descuento) {
                    alert("Código inválido o expirado");
                    return;
                }

                const order = this.pos.get_order();

                let total = order.get_total_with_tax();

                let nuevo_total = total;

                if (descuento.tipo === "porcentaje") {

                    nuevo_total = total - (total * descuento.valor / 100);

                } else {

                    nuevo_total = total - descuento.valor;

                }

                // redondear
                nuevo_total = Math.round(nuevo_total);

                const descuento_aplicado = total - nuevo_total;

                order.add_product(this.pos.db.get_product_by_id(descuento.producto_descuento_id), {
                    price: -descuento_aplicado,
                    quantity: 1
                });

                alert("Descuento aplicado correctamente");

            }

            catch (error) {

                console.error(error);
                alert("Error validando el código");

            }

        }

    }

});