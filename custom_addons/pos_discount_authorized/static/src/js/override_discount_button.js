/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ConfirmPopup } from "@point_of_sale/app/components/popups/confirm_popup/confirm_popup";
import { useService } from "@web/core/utils/hooks";
import { DiscountButton } from "@point_of_sale/app/screens/product_screen/control_buttons/discount_button";

const rpc = require("web.rpc");

DiscountButton.prototype.onClick = async function () {
    const dialog = this.env.services.dialog;

    const { confirmed, value } = await dialog.prompt({
        title: "Código de autorización",
        body: "Ingrese el código autorizador:",
    });

    if (!confirmed) return;

    const result = await this.env.services.rpc("/web/dataset/call_kw", {
        model: "pos.discount.code",
        method: "search_read",
        args: [[["code", "=", value.trim().toUpperCase()]], ["code", "used", "expired"]],
    });

    if (!result.length) {
        dialog.alert("Código inválido");
        return;
    }

    if (result[0].used || result[0].expired) {
        dialog.alert("Código expirado o ya utilizado");
        return;
    }

    // ⚠️ Si el código es válido → seguir con el descuento normal
    super.onClick();
};
/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ConfirmPopup } from "@point_of_sale/app/components/popups/confirm_popup/confirm_popup";
import { useService } from "@web/core/utils/hooks";
import { DiscountButton } from "@point_of_sale/app/screens/product_screen/control_buttons/discount_button";

const rpc = require("web.rpc");

DiscountButton.prototype.onClick = async function () {
    const dialog = this.env.services.dialog;

    const { confirmed, value } = await dialog.prompt({
        title: "Código de autorización",
        body: "Ingrese el código autorizador:",
    });

    if (!confirmed) return;

    const result = await this.env.services.rpc("/web/dataset/call_kw", {
        model: "pos.discount.code",
        method: "search_read",
        args: [[["code", "=", value.trim().toUpperCase()]], ["code", "used", "expired"]],
    });

    if (!result.length) {
        dialog.alert("Código inválido");
        return;
    }

    if (result[0].used || result[0].expired) {
        dialog.alert("Código expirado o ya utilizado");
        return;
    }

    // ⚠️ Si el código es válido → seguir con el descuento normal
    super.onClick();
};
