/** @odoo-module **/

import * as Chrome from "@punto_de_venta/../tests/tours/helpers/ChromeTourMethods";
import * as ProductScreen from "@punto_de_venta/../tests/tours/helpers/ProductScreenTourMethods";
import { registry } from "@web/core/registry";

registry.category("web_tour.tours").add("chrome_without_cash_move_permission", {
    test: true,
    url: "/pos/ui",
    steps: () =>
        [
            ProductScreen.confirmOpeningPopup(),
            Chrome.clickMenuButton(),
            Chrome.isCashMoveButtonHidden(),
        ].flat(),
});
