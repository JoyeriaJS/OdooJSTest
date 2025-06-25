odoo.define('pos_qr_auth_no_wizard.qr_auth', function(require) {
    'use strict';
    const models = require('point_of_sale.models');
    const Popup = require('point_of_sale.popups');
    const _super_pos = models.PosModel.prototype;
    const _super_line = models.Orderline.prototype;

    models.PosModel = models.PosModel.extend({
        initialize: function(session, attributes) {
            _super_pos.initialize.call(this, session, attributes);
            Popup.showPopup(this, 'TextInputPopup', {
                title: 'Escanea tu QR de vendedora',
                body: 'Por favor escanea tu código QR',
                confirmText: 'Confirmar',
            }).then(data => this.rpc({
                model: 'joyeria.vendedora',
                method: 'search_read',
                args: [[['codigo_qr','=',data]], ['id','name']],
            }).then(res => {
                if (res.length) {
                    this.config.vendedora_id = res[0].id;
                    Popup.showPopup(this, 'ConfirmPopup', {
                        title: 'Sesión iniciada', body: 'Bienvenida ' + res[0].name,
                    });
                } else {
                    Popup.showPopup(this, 'ErrorPopup', {
                        title: 'QR inválido', body: 'Vendedora no encontrada',
                    });
                }
            }));
        },
    });

    models.Orderline = models.Orderline.extend({
        set_discount: function(discount) {
            if (!this.pos.config.vendedora_id) {
                this.pos.gui.show_popup('ErrorPopup', {
                    title: 'Descuento no permitido', body: 'Escanea QR antes de aplicar descuento',
                });
                return;
            }
            return _super_line.set_discount.call(this, discount);
        },
    });
});