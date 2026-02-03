/** @odoo-module **/

// Esperar a que el POS cargue
odoo.define("pos_discount_authorized.discount_hook", function (require) {
    "use strict";

    const models = require("point_of_sale.models");

    // Guardamos la función original
    const _super_order = models.Order.prototype.set_discount;

    models.Order.prototype.set_discount = async function (discount) {

        // permitir sin autorización hasta 10%
        if (discount <= 10) {
            return _super_order.apply(this, arguments);
        }

        // pedir autorización
        const codigo = window.prompt("Descuento mayor al 10%. Ingrese código:");

        if (!codigo) {
            alert("Operación cancelada.");
            return;
        }

        // llamada RPC
        const valido = await this.pos.rpc({
            model: "pos.discount.authcode",
            method: "validar_codigo",
            args: [[], codigo, this.pos.get_cashier().id],
        });

        if (!valido) {
            alert("Código inválido o expirado.");
            return;
        }

        return _super_order.apply(this, arguments);
    };
});
