odoo.define("pos_discount_authorized.discount_hook", function (require) {
    "use strict";

    const models = require("point_of_sale.models");
    const rpc = require("web.rpc");

    const _super_order = models.Order.prototype.set_discount;

    models.Order.prototype.set_discount = function (discount) {

        // ⚠ Detener DESCUENTOS de CUALQUIER TIPO si no hay código
        let codigo = window.prompt("Ingrese código de autorización:");

        if (!codigo) {
            alert("Descuento rechazado. No se ingresó código.");
            return;
        }

        // Llamada RPC al backend
        return rpc.query({
            model: "pos.discount.authcode",
            method: "validar_codigo",
            args: [codigo, this.pos.cashier.id],
        }).then((valid) => {
            if (valid) {
                return _super_order.apply(this, arguments);
            } else {
                alert("Código inválido o expirado.");
                return;
            }
        });
    };
});
