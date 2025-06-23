# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from . import models
from . import controllers
from . import report
from . import wizard
from odoo import api, SUPERUSER_ID


def uninstall_hook(env):
    #The search domain is based on how the sequence is defined in the _get_sequence_values method in /addons/point_of_sale/models/stock_warehouse.py
    env['ir.sequence'].search([('name', 'ilike', '%Picking POS%'), ('prefix', 'ilike', '%/POS/%')]).unlink()

# pos_custom/__init__.py
def pre_init_hook(cr):
    # eliminar el add-on instalado
    env = api.Environment(cr, SUPERUSER_ID, {})
    mod = env['ir.module.module'].search([('name','=','point_of_sale')], limit=1)
    if mod:
        mod.button_uninstall()