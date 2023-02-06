# -*- coding: utf-8 -*-
{
    'name': "Asian Quotation",
    'version': '0.1',
    'depends': ['base', 'product', 'asia_sale', 'asia_contract', 'asia_group'],
    'data': [
        'security/rules.xml',
        'security/ir.model.access.csv',
        'views/assets.xml',
        'data/default_vehicle_price.xml',
        'views/asian_quotation_views.xml',
        'views/default_vehicle_price.xml',
        # 'views/asian_spreadsheet_option_views.xml',
    ],
    'auto_install': False,
    'application': True,
    'installable': True,
}
