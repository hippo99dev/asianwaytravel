from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    asian_quotation_id = fields.Many2one(string='Asian Quotation', comodel_name='asian.quotation')
    asian_spreadsheet_option_id = fields.Many2one(string='Asian Spreadsheet Option', comodel_name='asian.spreadsheet.option')
