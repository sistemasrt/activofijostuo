from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'


    is_fixed_active = fields.Boolean(
        string='Es Activo Fijo',
    )
    is_maintenance = fields.Boolean(
        string='Mantenimiento',
    )

    account_asset = fields.Boolean(
        string='Activo creado',
    )

    account_asset_id = fields.Many2one(
        'account.asset',
        readonly=True, 
        string='Activo fijo',
    )
    maintenance_equipment_id = fields.Many2one(
        'maintenance.equipment',
        readonly=True, 
        string='Mantenimiento',
    )

    property_stock_inventory_fixed_active = fields.Many2one(
        'stock.location', "Almacen",
        readonly=True,   
        )
    partner_id = fields.Many2one(
        'res.partner',
        string='Responsable',
    )
    note = fields.Text(
        string='Descripción',
        related="account_asset_id.note",
        store=True,
    )

    barcode_assets = fields.Char(
        string='Codigo',
        related="account_asset_id.barcode",
        store=True,
    )
    image_barcode = fields.Binary(
        string='Imagen',
        attachment=True,
        store=True,
        related="account_asset_id.image_barcode",

    )


    @api.constrains('is_fixed_active')
    def check_is_fixed_active(self):
        for rec in self:
            if rec.is_fixed_active == True:
                if rec.type != "product":
                    raise UserError(_("Tipo de producto debe ser Almacenable"))

