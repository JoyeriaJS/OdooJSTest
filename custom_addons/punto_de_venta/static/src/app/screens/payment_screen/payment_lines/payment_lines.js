/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { NumberPopup } from "@punto_de_venta/app/utils/input_popups/number_popup";
import { useService } from "@web/core/utils/hooks";
import { Component, useState } from "@odoo/owl";
import { usePos } from "@punto_de_venta/app/store/pos_hook";
import { parseFloat } from "@web/views/fields/parsers";

export class PaymentScreenPaymentLines extends Component {
    static template = "punto_de_venta.PaymentScreenPaymentLines";

    setup() {
        this.ui = useState(useService("ui"));
        this.popup = useService("popup");
        this.pos = usePos();
    }

    formatLineAmount(paymentline) {
        return this.env.utils.formatCurrency(paymentline.get_amount(), false);
    }
    selectedLineClass(line) {
        return { "payment-terminal": line.get_payment_status() };
    }
    unselectedLineClass(line) {
        return {};
    }
    async selectLine(paymentline) {
        this.props.selectLine(paymentline.cid);

        if (this.ui.isSmall) {
            const { confirmed, payload } = await this.popup.add(NumberPopup, {
                title: _t("New amount"),
                startingValue: paymentline.amount,
                isInputSelected: true,
                nbrDecimal: this.pos.currency.decimal_places,
            });

            if (confirmed) {
                this.props.updateSelectedPaymentline(parseFloat(payload));
            }
        }
        return;
    }
}
