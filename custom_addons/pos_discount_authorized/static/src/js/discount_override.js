/** @odoo-module **/

import { registry } from "@web/core/registry";
import { NumberPopup } from "@point_of_sale/app/utils/popups/number_popup";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";

console.log("🔥 POS DISCOUNT MODULE LOADED CORRECTLY 🔥");

patch(ProductScreen.prototype, "pos_discount_authorized", {
    async onClickDiscount(event) {

        const dialog = this.env.services.dialog;
        const rpc = this.env.services.rpc;

        // 1️⃣ Pedir código de autorización
        const { confirmed, value: code } = await dialog.prompt({
            title: "Código Autorizado",
            body: "Ingrese el código de autorización:",
        });

        if (!confirmed) return;

        const cleanCode = code.trim().toUpperCase();

        // 2️⃣ Revisar si el código existe y está disponible
        const result = await rpc("/web/dataset/call_kw", {
            model: "pos.discount.code",
            method: "search_read",
            args: [
                [["code", "=", cleanCode]],
                ["code", "discount_type", "discount_value", "used", "expired"]
            ],
        });

        if (!result.length) {
            await dialog.alert("Código inválido.");
            return;
        }

        const info = result[0];

        if (info.used || info.expired) {
            await dialog.alert("Código ya utilizado o expirado.");
            return;
        }

        // 3️⃣ Ahora sí pedir el porcentaje
        const { confirmed: ok2, payload: discount } = await this.showPopup(NumberPopup, {
            title: "Ingrese descuento (%) autorizado",
            startingValue: info.discount_value,
        });

        if (!ok2) return;

        // 4️⃣ Aplicar descuento con control nativo de Odoo
        super.onClickDiscount(event);

        // 5️⃣ Marcar el código como usado
        await rpc("/web/dataset/call_kw", {
            model: "pos.discount.code",
            method: "write",
            args: [[info.id], { used: true, fecha_uso: new Date() }],
        });

        await dialog.alert("Descuento aplicado correctamente.");
    }
});
