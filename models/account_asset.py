
import math
import re
from odoo import models, fields, api
import qrcode
import base64
from io import BytesIO



class AccountAsset(models.Model):
    _inherit = 'account.asset'

    name = fields.Char(
        string='Numero',
        copy=False,
        default='New',
        readonly=True
    )

    image_barcode = fields.Binary(
        string='Imagen',
        attachment=True,
        store=True,
    )


    
    product_id = fields.Many2one(
        'product.template',
        domain="[('is_fixed_active', '=', 'True'),('account_asset_id', '=', False)]",
        required=True,
        string='Nombre del modelo de activo',
    )

    barcode = fields.Char(
        string='Codigo',
        readonly=True,
    )

    property_stock_inventory_fixed_active = fields.Many2one(
        'stock.location', "Almacen",
        related="product_id.property_stock_inventory_fixed_active",
        store=True,
        )
    partner_id = fields.Many2one(
        'res.partner',
        string='Responsable',
        related="product_id.partner_id",
        store=True,
    )

    note = fields.Text(
        string='Descripción',
    )

    real_value = fields.Float(
        string='Valor Real',
    )

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence']\
                               .next_by_code('account.asset') or 'New'
        res = super(AccountAsset, self).create(vals)
        ean = generate_ean(str(res.id))
        res.product_id.write({'account_asset_id': res.id,'note':res.note,'barcode_assets': res.barcode,'account_asset': True})
        res.barcode = ean
        res.action_generate_imagen()
        return res

    def action_generate_imagen(self):
        for rec in self:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            codido = str(rec.product_id.name) + str("/") + str(rec.barcode) + str("/") + str(rec.property_stock_inventory_fixed_active.name) + str("/") + str(rec.partner_id.name) + str("/") + str(rec.acquisition_date)
            qr.add_data(codido)
            qr.make(fit=True)
            img = qr.make_image()
            temp = BytesIO()
            img.save(temp, format="PNG")
            qr_image = base64.b64encode(temp.getvalue())
            rec.image_barcode = qr_image


def ean_checksum(eancode):
    """returns the checksum of an ean string of length 13, returns -1 if
    the string has the wrong length"""
    if len(eancode) != 13:
        return -1
    oddsum = 0
    evensum = 0
    eanvalue = eancode
    reversevalue = eanvalue[::-1]
    finalean = reversevalue[1:]

    for i in range(len(finalean)):
        if i % 2 == 0:
            oddsum += int(finalean[i])
        else:
            evensum += int(finalean[i])
    total = (oddsum * 3) + evensum

    check = int(10 - math.ceil(total % 10.0)) % 10
    return check


def check_ean(eancode):
    """returns True if eancode is a valid ean13 string, or null"""
    if not eancode:
        return True
    if len(eancode) != 13:
        return False
    try:
        int(eancode)
    except:
        return False
    return ean_checksum(eancode) == int(eancode[-1])


def generate_ean(ean):
    """Creates and returns a valid ean13 from an invalid one"""
    if not ean:
        return "0000000000000"
    ean = re.sub("[A-Za-z]", "0", ean)
    ean = re.sub("[^0-9]", "", ean)
    ean = ean[:13]
    if len(ean) < 13:
        ean = ean + '0' * (13 - len(ean))
    return ean[:-1] + str(ean_checksum(ean))
