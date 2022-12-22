from odoo import models, fields, api


class AsianSpreadsheetTeamOption(models.Model):
    _name = 'asian.spreadsheet.team.option'
    _description = 'Asian Spreadsheet Team Option'

    name = fields.Char(string='Loại xe')
    profit = fields.Float(string='Lợi nhuận')
    car_4 = fields.Float(string='Xe 4 chỗ')
    car_7 = fields.Float(string='Xe 7 chỗ')
    car_16 = fields.Float(string='Xe 16 chỗ')
    car_29 = fields.Float(string='Xe 29 chỗ')
    car_35 = fields.Float(string='Xe 35 chỗ')
    car_45_1 = fields.Float(string='Xe 45 chỗ')
    car_45_2 = fields.Float(string='Xe 45 chỗ')
    car_45_3 = fields.Float(string='Xe 45 chỗ')
    car_45_4 = fields.Float(string='Xe 45 chỗ')
    apply = fields.Boolean(string='Tính báo giá')
    type_line = fields.Selection(string='Type Line', selection=[('by_type', 'Giá theo loại xe/KM'), ('by_team', 'Nhóm khách')])
    asian_spreadsheet_option_id = fields.Many2one(string='Asian Spreadsheet Option', comodel_name='asian.spreadsheet.option')
    asian_quotation_id = fields.Many2one(string='Asian Quotation', comodel_name='asian.quotation')
