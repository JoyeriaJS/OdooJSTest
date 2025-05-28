import odoo
import odoo.tools.config
from odoo import SUPERUSER_ID
from odoo.modules.registry import Registry

# Cambia por el nombre de tu base si no es 'railway'
db_name = 'railway'

odoo.tools.config['db_name'] = db_name
odoo.tools.config['db_host'] = 'postgres.railway.internal'
odoo.tools.config['db_port'] = '5432'
odoo.tools.config['db_user'] = 'postgres'
odoo.tools.config['db_password'] = 'zbjwUrZrVMmtaEjjTRKCdgMaQcXMRwLl'
odoo.tools.config['addons_path'] = 'odoo/addons,custom_addons'

# Inicializar el entorno
odoo.cli.server.setup_server_environment()
registry = Registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, SUPERUSER_ID, {})
    admin = env['res.users'].search([('login', '=', 'admin@example.com')], limit=1)
    if not admin:
        env['res.users'].create({
            'name': 'Administrador',
            'login': 'admin@example.com',
            'email': 'admin@example.com',
            'password': 'admin123',
            'groups_id': [(6, 0, [env.ref('base.group_system').id])],
        })
        print("✅ Usuario administrador creado")
    else:
        print("⚠️ Ya existe un usuario con login admin@example.com")
