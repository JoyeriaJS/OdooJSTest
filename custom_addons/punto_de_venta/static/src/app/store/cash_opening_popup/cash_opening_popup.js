/** @odoo-module */

import { AbstractAwaitablePopup } from "@punto_de_venta/app/popup/abstract_awaitable_popup";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@punto_de_venta/app/store/pos_hook";
import { MoneyDetailsPopup } from "@punto_de_venta/app/utils/money_details_popup/money_details_popup";
import { useState } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { Input } from "@punto_de_venta/app/generic_components/inputs/input/input";
import { parseFloat } from "@web/views/fields/parsers";

export class CashOpeningPopup extends AbstractAwaitablePopup {
    static template = "punto_de_venta.CashOpeningPopup";
    static components = { Input };
    static defaultProps = { cancelKey: false };

    setup() {
        super.setup();
        this.moneyDetails = null;
        this.pos = usePos();
        this.state = useState({
            notes: "",
            openingCash: this.env.utils.formatCurrency(
                this.pos.pos_session.cash_register_balance_start || 0,
                false
            ),
        });
        this.popup = useService("popup");
        this.orm = useService("orm");
        this.hardwareProxy = useService("hardware_proxy");
    }
    //@override
    async confirm() {
        this.pos.pos_session.state = "opened";
        this.orm.call("pos.session", "set_cashbox_pos", [
            this.pos.pos_session.id,
            parseFloat(this.state.openingCash),
            this.state.notes,
        ]);
        super.confirm();
    }
    async openDetailsPopup() {
        const action = _t("Cash control - opening");
        this.hardwareProxy.openCashbox(action);
        const { confirmed, payload } = await this.popup.add(MoneyDetailsPopup, {
            moneyDetails: this.moneyDetails,
            action: action,
        });
        if (confirmed) {
            const { total, moneyDetails, moneyDetailsNotes } = payload;
            this.state.openingCash = this.env.utils.formatCurrency(total, false);
            if (moneyDetailsNotes) {
                this.state.notes = moneyDetailsNotes;
            }
            this.moneyDetails = moneyDetails;
        }
    }
    handleInputChange() {
        if (!this.env.utils.isValidFloat(this.state.openingCash)) {
            return;
        }
        this.state.notes = "";
    }
}
