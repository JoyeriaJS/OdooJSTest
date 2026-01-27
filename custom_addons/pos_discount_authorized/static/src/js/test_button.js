/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class TestButton extends Component {

    setup() {
        console.log("🔥🔥 TEST BUTTON CARGADO Y MONTADO EN UI");
    }

    onClick() {
        alert("FUNCIONÓ! EL POS ESTÁ TOMANDO CUSTOMIZACIÓN 🔥");
    }
}

TestButton.template = "TestButtonTemplate";

registry.category("pos_screens").add("TestButton", {
    component: TestButton,
    position: "payment-buttons",
});
