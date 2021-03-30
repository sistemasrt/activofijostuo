
from odoo import _, api, fields, models

class AccountAssetFilter(models.TransientModel):
    _name = 'account.asset.filter.wizard'
    _description = "wizard para filtro activos fijos"

    def filter_account_asset(self):        
        
        return {
            'type': 'ir.actions.act_window',
            'name': "Activos Fijos",
            'view_type': 'form',
            'res_model': 'account.asset',
            'view_mode': 'tree,form',
            'target': 'current',
            'context':{'group_by':'partner_id'},
        
        }
            