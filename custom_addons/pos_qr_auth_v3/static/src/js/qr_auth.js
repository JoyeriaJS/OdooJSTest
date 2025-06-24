odoo.define('pos_qr_auth.qr_auth', function(require) {
    'use strict';
    const models = require('point_of_sale.models');
    const _super_pos = models.PosModel.prototype;
    const _super_line = models.Orderline.prototype;

    models.PosModel = models.PosModel.extend({
        initialize: function(session, attributes) {
            _super_pos.initialize.call(this, session, attributes);
            const self = this;
            this.chrome.setLoading(true);
            this.gui.show_popup('textinput', {
                title: 'Escanea tu QR de vendedora', body: 'Por favor escanea tu código QR', confirmText: 'Confirmar'
            }).then(function(code) {
                return self.rpc({
                    model: 'joyeria.vendedora',
                    method: 'search_read',
                    args: [[['codigo_qr','=',code]], ['id','name']],
                }).then(function(res) {
                    if (res.length) {
                        self.config.vendedora_id = res[0].id;
                        self.gui.show_popup('confirm', { title: 'Sesión iniciada', body: 'Bienvenida ' + res[0].name });
                    } else {
                        self.gui.show_popup('error', { title: 'QR inválido', body: 'Usuario no encontrado' });
                    }
                });
            }).finally(function() {
                self.chrome.setLoading(false);
            });
        },
    });

    models.Orderline = models.Orderline.extend({
        set_discount: function(discount) {
            if (!this.pos.config.vendedora_id) {
                this.gui.show_popup('error', {title: 'Descuento no permitido', body: 'Escanea QR antes de aplicar descuento'});
                return;
            }
            return _super_line.set_discount.call(this, discount);
        },
    });
});