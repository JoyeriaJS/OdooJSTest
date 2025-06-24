/** @odoo-module */

import { AbstractAwaitablePopup } from "@punto_de_venta/app/popup/abstract_awaitable_popup";
import { _t } from "@web/core/l10n/translation";

export class ConfirmPopup extends AbstractAwaitablePopup {
    static template = "punto_de_venta.ConfirmPopup";
    static defaultProps = {
        confirmText: _t("Ok"),
        cancelText: _t("Cancel"),
        title: _t("Confirm?"),
        body: "",
    };
}
