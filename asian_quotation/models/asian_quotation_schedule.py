from odoo import models, fields, api


class AsianQuotationSchedule(models.Model):
    _name = 'asian.quotation.schedule'
    _order = 'sequence,schedule_date_date'
    _description = 'Asian Quotation Schedule'

    sequence = fields.Integer(string='Sequence', default=0)
    schedule_date = fields.Integer(string='Ngày')
    schedule_act = fields.Text(string='Program Detail')
    note = fields.Text(string='Itinerary')
    customer_market = fields.Char(string='Thị trường khách')
    validate_season = fields.Selection(string="Thời gian hiệu lực", selection=[('peak_season', 'Mùa cao điểm'), ('low_season', 'Mùa thấp điểm')])
    meal_supplied = fields.Char(string='Bữa ăn')
    schedule_date_date = fields.Date(string='Date')
    weekday = fields.Char(string='Weekday')
    meal_ids = fields.Many2many(comodel_name='x.meal', string='Bữa ăn')
    template_id = fields.Many2one(string='Template', comodel_name='sale.order.template')

    asian_spreadsheet_option_id = fields.Many2one(string='Asian Spreadsheet Option', comodel_name='asian.spreadsheet.option', ondelete='cascade')
