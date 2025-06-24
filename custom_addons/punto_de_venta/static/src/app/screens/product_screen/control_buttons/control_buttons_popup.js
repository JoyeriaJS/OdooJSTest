/** @odoo-module */

import { AbstractAwaitablePopup } from "@punto_de_venta/app/popup/abstract_awaitable_popup";
import { _t } from "@web/core/l10n/translation";

export class ControlButtonPopup extends AbstractAwaitablePopup {
    static template = "punto_de_venta.ControlButtonPopup";
    static defaultProps = {
        cancelText: _t("Back"),
        controlButtons: [],
        confirmKey: false,
    };

    /**
     * @param {Object} props
     * @param {string} props.startingValue
     */
    setup() {
        super.setup();
        this.controlButtons = this.props.controlButtons;
    }
}
