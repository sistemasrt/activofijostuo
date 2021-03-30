from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    fixed_counts = fields.Integer(
        string='Activos fijos',
        compute='compute_count_fixed'
    )

    def compute_count_fixed(self):
        for record in self:
            record.fixed_counts = self.env['account.asset'].search_count(
                [('partner_id', '=', self.id)])


    def get_fixed(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Activos',
            'view_mode': 'tree,form',
            'res_model': 'account.asset',
            'domain': [('partner_id', '=', self.id)],
        }
