/** @odoo-module */

import { AbstractAwaitablePopup } from "@punto_de_venta/app/popup/abstract_awaitable_popup";
import { _t } from "@web/core/l10n/translation";

export class OrderImportPopup extends AbstractAwaitablePopup {
    static template = "punto_de_venta.OrderImportPopup";
    static defaultProps = {
        confirmText: _t("Ok"),
        cancelKey: false,
        body: "",
    };

    get unpaidSkipped() {
        return (
            (this.props.report.unpaid_skipped_existing || 0) +
            (this.props.report.unpaid_skipped_session || 0)
        );
    }
    getPayload() {}
}
