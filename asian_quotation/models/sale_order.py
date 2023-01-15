from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    asian_quotation_id = fields.Many2one(string='Asian Quotation', comodel_name='asian.quotation')
