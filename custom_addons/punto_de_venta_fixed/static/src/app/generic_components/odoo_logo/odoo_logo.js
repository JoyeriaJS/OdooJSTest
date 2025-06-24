/** @odoo-module */

import { Component } from "@odoo/owl";

export class OdooLogo extends Component {
    static template = "punto_de_venta.OdooLogo";
    static props = {
        class: { type: String, optional: true },
        style: { type: String, optional: true },
        monochrome: { type: Boolean, optional: true },
    };
    static defaultProps = {
        class: "",
        style: "",
        monochrome: false,
    };
}
