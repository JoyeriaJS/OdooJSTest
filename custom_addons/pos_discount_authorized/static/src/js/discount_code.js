
odoo.define('pos_discount_authorized.DiscountCodePopup', function(require){
    "use strict";
    const rpc = require('web.rpc');
    const { Gui } = require('point_of_sale.Gui');
    const chrome = require('point_of_sale.Chrome');

    chrome.Chrome.include({
        start: async function(){
            await this._super(...arguments);

            this.addActionButton({
                name: 'discount_code',
                label: 'Código Descuento',
                icon: 'fa fa-tag',
                action: async ()=>{
                    const { confirmed, payload } = await Gui.showPopup('TextInputPopup', {
                        title: 'Ingresar código de descuento'
                    });

                    if (!confirmed) return;

                    let codigo = payload;

                    let result = await rpc.query({
                        model: 'pos.discount.code',
                        method: 'search_read',
                        args: [[['code','=',codigo]], ['code','discount_type','discount_value','used','expired']],
                    });

                    if(result.length === 0){
                        Gui.showPopup('ErrorPopup', { title: 'Código inválido', body: 'No existe el código.' });
                        return;
                    }

                    let data = result[0];

                    if(data.used || data.expired){
                        Gui.showPopup('ErrorPopup', { title: 'Código inválido', body: 'Código usado o expirado.' });
                        return;
                    }

                    let order = this.env.pos.get_order();

                    if(data.discount_type === "percent"){
                        order.add_global_discount(data.discount_value);
                    } else {
                        order.add_cashpayment(-data.discount_value);
                    }

                    Gui.showPopup('ConfirmPopup', { title: 'Descuento aplicado', body: 'Código aplicado correctamente.' });

                    await rpc.query({
                        model: 'pos.discount.code',
                        method: 'write',
                        args: [[data.id], { used: true, fecha_uso: new Date() }],
                    });
                }
            });
        }
    });
});
