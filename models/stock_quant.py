from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.model
    def create(self, vals):
       
        res = super(StockQuant, self).create(vals)
        if res.product_id.is_fixed_active == True:
            res.product_id.write({'property_stock_inventory_fixed_active': res.location_id.id})
        return res


    def write(self, values):        
        for rec in self:
            if rec.product_id.is_fixed_active == True:
                rec.product_id.write({'property_stock_inventory_fixed_active': rec.location_id.id})

        return super(StockQuant, self).write(values)
