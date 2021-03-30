
from odoo import models, fields, api
import qrcode
import base64
from io import BytesIO


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    name = fields.Char(
        string='Numero',
        copy=False,
        default='New',
        readonly=True
    )

    
    product_id = fields.Many2one(
        'product.template',
        domain="[('is_maintenance', '=', 'True'),('account_asset_id', '!=', False),('maintenance_equipment_id', '=', False)]",
        required=True,
        string='Nombre del modelo de activo',
    )

    is_fixed_active = fields.Boolean(
        string='Activo fijo',
        related="product_id.is_fixed_active",
        store=True,
    )
  

    property_stock_inventory_fixed_active = fields.Many2one(
        'stock.location', "Almacen",
        related="product_id.property_stock_inventory_fixed_active",
        store=True,
        )
    partner_id_related = fields.Many2one(
        'res.partner',
        string='Responsable',
        related="product_id.partner_id",
        store=True,
    )

    account_asset_id = fields.Many2one(
        'account.asset',
        readonly=True, 
        string='Activo fijo',
        related="product_id.account_asset_id",
        store=True,
    )

    barcode = fields.Char(
        string='Codigo',
        readonly=True,
        related="product_id.account_asset_id.barcode",
        store=True,
    )
    image_barcode = fields.Binary(
        string='Imagen',
        attachment=True,        
        related="product_id.account_asset_id.image_barcode",
        store=True,

    )

    notes = fields.Text(
        string='Descripción',
        related="product_id.account_asset_id.note",
        store=True,
    )

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence']\
                               .next_by_code('maintenance.equipment') or 'New'
        res = super(MaintenanceEquipment, self).create(vals)
        res.product_id.write({'maintenance_equipment_id': res.id})
        return res



