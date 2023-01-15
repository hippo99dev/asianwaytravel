# -*- coding: utf-8 -*-
{
    'name': "Asian Sale Purchase Payment",
    'version': '0.1',
    'depends': ['base', 'product', 'sale', 'purchase', 'sale_purchase', 'asia_sale', 'asia_purchase'],
    'data': [
        'security/ir_rule.xml',
        'data/ir_attachment.xml',
        'views/sale_order_payment_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/guider_contract_wizard_views.xml',
    ],
    'auto_install': False,
    'application': False,
    'installable': True,
}
