odoo.define('pos_qr_auth.qr_auth', function(require){
    'use strict';
    const models = require('point_of_sale.models');
    const Popup = require('point_of_sale.popups');

    models.PosModel = models.PosModel.extend({
        initialize: function(session, attributes){
            this._super(session, attributes);
            const self = this;
            this.chrome.setLoading(true);
            Popup.showPopup(self, 'TextInputPopup', {
                title: 'Escanea tu QR de vendedora',
                body: 'Por favor escanea el QR para iniciar sesión',
                confirmText: 'Confirmar',
                cancelText: 'Cancelar',
            }).then(function(data){
                const code = data || '';
                if(code.startsWith('VEND-')){
                    const vend_id = parseInt(code.replace('VEND-',''));
                    return self.rpc({
                        model: 'joyeria.vendedora',
                        method: 'search_read',
                        args: [[['id','=',vend_id]], ['name']],
                    }).then((res) => {
                        if(res.length){
                            self.config.vendedora_id = vend_id;
                        } else {
                            self.gui.show_popup('ErrorPopup',{
                                title:'QR inválido',
                                body:'Vendedora no encontrada',
                            });
                        }
                    });
                } else {
                    self.gui.show_popup('ErrorPopup',{
                        title:'QR inválido',
                        body:'Formato de QR no reconocido',
                    });
                }
            }).finally(function(){
                self.chrome.setLoading(false);
            });
        },
    });

    models.Orderline = models.Orderline.extend({
        set_discount: function(discount){
            if(!this.pos.config.vendedora_id){
                this.pos.gui.show_popup('ErrorPopup',{
                    title:'Descuento no permitido',
                    body:'Debe escanear QR antes de aplicar descuentos',
                });
                return;
            }
            return this._super(discount);
        },
    });
});