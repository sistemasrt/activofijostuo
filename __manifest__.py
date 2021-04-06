# -*- coding: utf-8 -*-
{
    'name': "fixed_assets",

    'summary': """""",

    'description': """
        Relacion activos fijos, fantenimiento y contactos
    """,

    'author': "Victor Soto by Tuodoo",
    'website': "http://www.tuodoo.com",
    'category': 'Account',
    'version': '0.1',
    'depends': ['product','account','base','account_asset'],
    'data': [
        'views/product_template.xml',
        'views/account_asset.xml',
        'views/res_partner.xml',
        'views/maintenance_equipment.xml',
        'data/data.xml',
        'wizard/account_asset_filter_wizard.xml',
        'report/report_account_asset.xml',
        'report/report_account_asset_product.xml',
        'report/report_account_asset_maintenance.xml',
    ],
}
