# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from . import models,api,SUPERUSER_ID
from . import controllers
from . import report
from . import wizard



def uninstall_hook(env):
    #The search domain is based on how the sequence is defined in the _get_sequence_values method in /addons/point_of_sale/models/stock_warehouse.py
    env['ir.sequence'].search([('name', 'ilike', '%Picking POS%'), ('prefix', 'ilike', '%/POS/%')]).unlink()

# __init__.py de tu módulo custom
def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    pos = env['ir.module.module'].search([('name', '=', 'point_of_sale')])
    if pos and pos.state == 'installed' and pos.id != env.ref('your_module.point_of_sale').id:
        pos.button_immediate_uninstall()