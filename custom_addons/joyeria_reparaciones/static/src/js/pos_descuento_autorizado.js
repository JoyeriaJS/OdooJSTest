/* @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { useService } from "@web/core/utils/hooks";
import { TextInputPopup } from "@point_of_sale/app/utils/input_popups/text_input_popup";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

patch(PaymentScreen.prototype, {

    setup() {
        super.setup();
        this.rpc = useService("rpc");
        this.orm = useService("orm");
        this.popup = useService("popup");
    },

    async validateOrder(isForceValidate) {

        const order = this.currentOrder;

        // ==============================
        // VALIDACIÓN 50% PRECIO MÍNIMO
        // ==============================

        const lines = order.get_orderlines();

        for (let line of lines) {

            const esProductoRMA =
                line.product &&
                line.product.display_name &&
                line.product.display_name.trim() === "Producto RMA";

            const esLineaAuxiliarRMA =
                line.es_linea_rma_aux === true &&
                (
                    line.tipo_linea_rma === "abono" ||
                    line.tipo_linea_rma === "subtotal"
                );

            const esProductoGasto = line.es_producto_gasto === true;

            if (esProductoRMA || esLineaAuxiliarRMA || esProductoGasto) {
                continue;
            }

            const precioOriginal = line.product.lst_price || 0;
            const precioVenta = line.get_unit_price();
            const subtotal = line.get_price_with_tax();

            const pricelistName = (order.pricelist && order.pricelist.name || "").toLowerCase();

            const esListaExcepcion =
                pricelistName.includes("mayorista") ||
                pricelistName.includes("preferente") ||
                pricelistName.includes("interno");

            // ==============================
            // 🚨 BLOQUEO REAL PRECIO 0 (FIX BUG ⌫)
            // ==============================

            if (precioVenta <= 0 || subtotal <= 0) {
                await this.popup.add(ErrorPopup, {
                    title: "Precio inválido",
                    body: "No se puede vender '" + line.product.display_name + "' con precio 0 o inválido",
                });
                return;
            }

            // ==============================
            // VALIDACIÓN 50%
            // ==============================

            if (!esListaExcepcion && precioVenta < (precioOriginal * 0.5)) {

                await this.popup.add(ErrorPopup, {
                    title: "Precio inválido",
                    body: "No se puede vender '" + line.product.display_name + "' bajo el 50%",
                });

                return;
            }
        }

        // ==============================
        // DESCUENTO AUTORIZADO
        // ==============================

        if (!order.descuento_aplicado) {

            const paymentlines = order.paymentlines || [];
            let metodoPermitido = false;

            paymentlines.forEach(line => {
                const name = (line.payment_method.name || "").toLowerCase();

                if (
                    name.includes("efectivo") ||
                    name.includes("transferencia") ||
                    name.includes("credito") ||
                    name.includes("crédito")
                ) {
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
                        alert("Código inválido o ya utilizado");
                    } else {

                        const metodosOrden = paymentlines.map(
                            l => (l.payment_method.name || "").toLowerCase().trim()
                        );

                        const metodosPermitidos = (descuento.metodos_pago_nombres || []).map(
                            m => (m || "").toLowerCase().trim()
                        );

                        const metodoValido = metodosOrden.some(m =>
                            metodosPermitidos.includes(m)
                        );

                        if (!metodoValido) {
                            alert("Este descuento no es válido para el método de pago seleccionado.");
                        } else {

                            if (descuento.tipo_descuento === "porcentaje") {

                                const porcentaje = parseFloat(descuento.porcentaje);

                                lines.forEach(line => {
                                    line.set_discount(porcentaje);
                                });

                            }

                            if (descuento.tipo_descuento === "monto") {

                                const total = order.get_total_with_tax();
                                const porcentaje = (descuento.monto / total) * 100;

                                lines.forEach(line => {
                                    line.set_discount(porcentaje);
                                });

                            }

                            await this.rpc("/pos/usar_descuento", {
                                descuento_id: descuento.id
                            });

                            order.descuento_aplicado = true;

                            alert("Descuento aplicado correctamente");
                        }
                    }
                }
            }
        }

        // ==============================
        // 🔐 VENDEDORA
        // ==============================

        if (!order.vendedora_id) {

            const { confirmed, payload } = await this.popup.add(TextInputPopup, {
                title: "Clave de Vendedora",
                body: "Ingrese o escanee la clave",
                isPassword: true,
            });

            if (!confirmed || !payload) {
                return;
            }

            const result = await this.orm.call(
                'joyeria.vendedora',
                'validar_vendedora_pos',
                [payload.trim()]
            );

            if (!result) {
                await this.popup.add(ErrorPopup, {
                    title: "Clave inválida",
                    body: "No se encontró una vendedora con esa clave.",
                });
                return;
            }

            order.vendedora_id = result.id;
            order.vendedora_name = result.name;
        }

        return await super.validateOrder(isForceValidate);
    }

});