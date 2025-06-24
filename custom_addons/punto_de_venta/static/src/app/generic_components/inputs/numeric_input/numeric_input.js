/** @odoo-module */

import { TModelInput } from "@punto_de_venta/app/generic_components/inputs/t_model_input";

export class NumericInput extends TModelInput {
    static template = "punto_de_venta.NumericInput";
    static props = {
        ...super.props,
        class: { type: String, optional: true },
        min: { type: Number, optional: true },
    };
    static defaultProps = { class: "" };
    parseInt(value) {
        return parseInt(value);
    }
}
