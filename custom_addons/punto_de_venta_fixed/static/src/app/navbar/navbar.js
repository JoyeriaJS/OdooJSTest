/** @odoo-module */

import { usePos } from "@punto_de_venta/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { isMobileOS } from "@web/core/browser/feature_detection";

import { CashierName } from "@punto_de_venta/app/navbar/cashier_name/cashier_name";
import { CustomerFacingDisplayButton } from "@punto_de_venta/app/navbar/customer_facing_display_button/customer_facing_display_button";
import { ProxyStatus } from "@punto_de_venta/app/navbar/proxy_status/proxy_status";
import { SaleDetailsButton } from "@punto_de_venta/app/navbar/sale_details_button/sale_details_button";
import { SyncNotification } from "@punto_de_venta/app/navbar/sync_notification/sync_notification";
import { CashMovePopup } from "@punto_de_venta/app/navbar/cash_move_popup/cash_move_popup";
import { TicketScreen } from "@punto_de_venta/app/screens/ticket_screen/ticket_screen";
import { BackButton } from "@punto_de_venta/app/navbar/back_button/back_button";
import { Component, useState, useExternalListener } from "@odoo/owl";
import { ClosePosPopup } from "@punto_de_venta/app/navbar/closing_popup/closing_popup";
import { _t } from "@web/core/l10n/translation";
import { ProductScreen } from "@punto_de_venta/app/screens/product_screen/product_screen";

export class Navbar extends Component {
    static template = "punto_de_venta.Navbar";
    static components = {
        // FIXME POSREF remove some of these components
        CashierName,
        CustomerFacingDisplayButton,
        ProxyStatus,
        SaleDetailsButton,
        SyncNotification,
        BackButton,
    };
    static props = {};
    setup() {
        this.pos = usePos();
        this.ui = useState(useService("ui"));
        this.debug = useService("debug");
        this.popup = useService("popup");
        this.notification = useService("pos_notification");
        this.hardwareProxy = useService("hardware_proxy");
        this.state = useState({ isMenuOpened: false });
        useExternalListener(window, "mouseup", this.onOutsideClick);
    }

    onOutsideClick() {
        if (this.state.isMenuOpened) {
            this.state.isMenuOpened = false;
        }
    }

    get customerFacingDisplayButtonIsShown() {
        return this.pos.config.iface_customer_facing_display && !isMobileOS();
    }
    get showCashMoveButton() {
        return Boolean(this.pos?.config?.cash_control && this.pos?.config?.has_cash_move_permission);
    }
    onCashMoveButtonClick() {
        this.hardwareProxy.openCashbox(_t("Cash in / out"));
        this.popup.add(CashMovePopup);
    }
    async onTicketButtonClick() {
        if (this.isTicketScreenShown) {
            this.pos.closeScreen();
        } else {
            if (this._shouldLoadOrders()) {
                try {
                    this.pos.setLoadingOrderState(true);
                    const message = await this.pos._syncAllOrdersFromServer();
                    if (message) {
                        this.notification.add(message, 5000);
                    }
                } finally {
                    this.pos.setLoadingOrderState(false);
                    this.pos.showScreen("TicketScreen");
                }
            } else {
                this.pos.showScreen("TicketScreen");
            }
        }
    }

    _shouldLoadOrders() {
        return this.pos.config.trusted_config_ids.length > 0;
    }

    get isTicketScreenShown() {
        return this.pos.mainScreen.component === TicketScreen;
    }

    get orderCount() {
        return this.pos.get_order_list().length;
    }

    isBurgerMenuClosed() {
        return !this.state.isMenuOpened;
    }

    closeMenu() {
        this.state.isMenuOpened = false;
    }

    openMenu() {
        this.state.isMenuOpened = true;
    }

    async closeSession() {
        const info = await this.pos.getClosePosInfo();
        this.popup.add(ClosePosPopup, { ...info });
    }

    showBackButton() {
        return this.pos.showBackButton() && this.ui.isSmall;
    }

    toggleProductView() {
        const newView = this.pos.productListView === "grid" ? "list" : "grid";
        window.localStorage.setItem("productListView", newView);
        this.pos.productListView = this.pos.productListView === "grid" ? "list" : "grid";
    }

    get showToggleProductView() {
        return this.pos.mainScreen.component === ProductScreen && this.ui.isSmall;
    }
}
