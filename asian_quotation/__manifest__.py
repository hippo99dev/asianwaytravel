# -*- coding: utf-8 -*-
{
    'name': "Asian Quotation",
    'version': '0.1',
    'depends': ['base', 'product', 'asia_sale', 'asia_contract'],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/asian_quotation_views.xml',
        # 'views/asian_spreadsheet_option_views.xml',
    ],
    'auto_install': False,
    'application': True,
    'installable': True,
}
