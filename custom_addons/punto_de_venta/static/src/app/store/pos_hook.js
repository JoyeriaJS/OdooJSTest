/** @odoo-module */

import { useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

/**
 * @returns {import("@punto_de_venta/app/store/pos_store").PosStore}
 */
export function usePos() {
    return useState(useService("pos"));
}
