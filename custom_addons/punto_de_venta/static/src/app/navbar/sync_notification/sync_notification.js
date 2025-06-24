/** @odoo-module */

import { Component } from "@odoo/owl";
import { usePos } from "@punto_de_venta/app/store/pos_hook";

export class SyncNotification extends Component {
    static template = "punto_de_venta.SyncNotification";

    setup() {
        this.pos = usePos();
    }
    get sync() {
        return this.pos.synch;
    }
    onClick() {
        if (this.pos.synch.status !== "connected") {
            this.pos.showOfflineWarning = true;
        }
        this.pos.push_orders({ show_error: true });
    }
}
