/** @odoo-module */

import { AbstractAwaitablePopup } from "@punto_de_venta/app/popup/abstract_awaitable_popup";
import { useState } from "@odoo/owl";
import { usePos } from "@punto_de_venta/app/store/pos_hook";
import { floatIsZero } from "@web/core/utils/numbers";
import { NumericInput } from "@punto_de_venta/app/generic_components/inputs/numeric_input/numeric_input";

export class MoneyDetailsPopup extends AbstractAwaitablePopup {
    static template = "punto_de_venta.MoneyDetailsPopup";
    static components = { NumericInput };

    setup() {
        super.setup();
        this.pos = usePos();
        this.currency = this.pos.currency;
        this.state = useState({
            moneyDetails: this.props.moneyDetails
                ? { ...this.props.moneyDetails }
                : Object.fromEntries(this.pos.bills.map((bill) => [bill.value, 0])),
        });
    }
    computeTotal(moneyDetails = this.state.moneyDetails) {
        return Object.entries(moneyDetails).reduce((total, [value, inputQty]) => {
            const quantity = isNaN(inputQty) ? 0 : inputQty;
            return total + parseFloat(value) * quantity;
        }, 0);
    }
    //@override
    async getPayload() {
        let moneyDetailsNotes = !floatIsZero(this.computeTotal(), this.currency.decimal_places)
            ? "Money details: \n"
            : null;
        this.pos.bills.forEach((bill) => {
            if (this.state.moneyDetails[bill.value]) {
                moneyDetailsNotes += `  - ${
                    this.state.moneyDetails[bill.value]
                } x ${this.env.utils.formatCurrency(bill.value)}\n`;
            }
        });
        return {
            total: this.computeTotal(),
            moneyDetailsNotes,
            moneyDetails: { ...this.state.moneyDetails },
            action: this.props.action,
        };
    }
    async cancel() {
        super.cancel();
        if (
            this.pos.config.iface_cashdrawer &&
            this.pos.hardwareProxy.connectionInfo.status === "connected"
        ) {
            this.pos.logEmployeeMessage(this.props.action, "ACTION_CANCELLED");
        }
    }
    _parseFloat(value) {
        return parseFloat(value);
    }
}
