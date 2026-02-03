/** @odoo-module **/

odoo.define("pos_discount_authorized.discount_hook", function (require) {
    "use strict";

    const models = require("point_of_sale.models");
    const rpc = require("web.rpc");

    // Guardamos la función original
    const _super_orderline = models.Orderline.prototype.set_discount;

    models.Orderline.prototype.set_discount = function (discount) {

        const self = this;

        // Si el descuento es menor o igual a 10%, permitir normal
        if (discount <= 10) {
            return _super_orderline.apply(this, arguments);
        }

        // Solicitar código
        return new Promise(function (resolve, reject) {

            const code = window.prompt("Descuento mayor al 10%. Ingrese código de autorización:");

            if (!code) {
                alert("Operación cancelada.");
                return resolve(false);
            }

            // Validación en backend
            rpc.query({
                model: "pos.discount.authcode",
                method: "validar_codigo",
                args: [[], code, self.pos.get_cashier().id],
            })
            .then(function (valid) {
                if (valid) {
                    resolve(_super_orderline.apply(self, arguments));
                } else {
                    alert("Código inválido, usado o expirado.");
                    resolve(false);
                }
            })
            .catch(function () {
                alert("Error de comunicación con el servidor.");
                resolve(false);
            });
        });
    };
});
