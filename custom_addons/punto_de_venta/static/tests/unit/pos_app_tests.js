/** @odoo-module */
import { Chrome } from "@punto_de_venta/app/pos_app";
import { getFixture, mount } from "@web/../tests/helpers/utils";
import { makeTestEnv } from "@web/../tests/helpers/mock_env";
import { registry } from "@web/core/registry";
import { posService } from "@punto_de_venta/app/store/pos_store";
import { numberBufferService } from "@punto_de_venta/app/utils/number_buffer_service";
import { barcodeReaderService } from "@punto_de_venta/app/barcode/barcode_reader_service";
import { EventBus } from "@odoo/owl";
import { uiService } from "@web/core/ui/ui_service";
import { popupService } from "@punto_de_venta/app/popup/popup_service";

const mockContextualUtilsService = {
    dependencies: ["pos", "localization"],
    start(env, { pos, localization }) {
        const formatCurrency = (value, hasSymbol = true) => {
            return "dummy";
        };
        const floatIsZero = (value) => {
            return value === 0;
        };
        env.utils = {
            formatCurrency,
            floatIsZero,
        };
    },
};

QUnit.module("Chrome", {
    beforeEach() {
        registry
            .category("services")
            .add("pos", posService)
            .add("number_buffer", numberBufferService)
            .add("barcode_reader", barcodeReaderService)
            .add("ui", uiService)
            .add("popup", popupService)
            .add("contextual_utils_service", mockContextualUtilsService)
            .add("barcode", {
                start() {
                    return { bus: new EventBus() };
                },
            })
            .add("bus_service", {
                start() {
                    return { addChannel: () => {}, addEventListener: () => {} };
                },
            })
            .add("printer", {
                start() {
                    return {
                        printWeb: () => {},
                        printHtml: () => {},
                        printHtmlAlternative: () => {},
                    };
                },
            });

        for (const service of ["hardware_proxy", "debug", "pos_notification", "sound", "action"]) {
            registry.category("services").add(service, {
                start() {
                    return {};
                },
            });
        }
    },
});

const serverData = {
    models: { "product.product": { fields: {}, records: [] } },
};

QUnit.test("mount the Chrome", async (assert) => {
    const fixture = getFixture();
    assert.verifySteps([]);
    await mount(Chrome, fixture, {
        env: await makeTestEnv({ serverData }),
        test: true,
        props: { disableLoader: () => assert.step("disable loader") },
    });
    assert.containsOnce(fixture, ".pos");
    assert.verifySteps(["disable loader"]);
});
