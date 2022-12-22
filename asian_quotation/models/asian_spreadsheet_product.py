from odoo import models, fields, api
from odoo.osv import expression


class AsianSpreadsheetProduct(models.Model):
    _name = 'asian.spreadsheet.product'
    _description = 'Asian Spreadsheet Product'
    _rec_name = 'date_number'
    _order = 'sequence'

    date_number = fields.Char('Số ngày')
    travel_itinerary = fields.Text('Lịch trình')

    hotel_price = fields.Float(string='Giá khách sạn')
    # hotel_price = fields.Float(string='Giá khách sạn', compute='_compute_hotel_price', store=True)
    hotel_id = fields.Many2one(string='Tên khách sạn', comodel_name='product.product', domain=[('product_types', '=', 'hotel')])
    meal_price = fields.Float(string='Nhà hàng')
    ticket_price = fields.Float(string='Vé thắng cảnh')
    show_price = fields.Float(string='Show')
    transit_price = fields.Float(string='Xe vận chuyển')
    transport_price = fields.Float(string='Di chuyển')
    guide_price = fields.Float(string='Hướng dẫn viên')

    sequence = fields.Integer(string='Sequence', default=10)
    type_line = fields.Selection(string='Loại dòng', selection=[('formula', 'Công thức'), ('net', 'Giá Net')], readonly=True)
    asian_quotation_id = fields.Many2one(string='Asian Quotation', comodel_name='asian.quotation')
    asian_spreadsheet_option_id = fields.Many2one(string='Asian Spreadsheet Option', comodel_name='asian.spreadsheet.option')

    @api.onchange('hotel_id')
    def onchange_hotel_id(self):
        today = fields.Date.today()
        domain = [
            '&',
            ('contract_id.state', 'in', ['new', 'doing']),
            '|',
            '&',
            ('date_start', '<=', today),
            ('date_end', '>=', today),
            ('date_start', '>=', today),
        ]
        for rec in self:
            suppliers = self.env['product.supplierinfo'].search(expression.AND([[('product_id', '=', rec.hotel_id.id)], domain]), order='price')
            if suppliers:
                rec.hotel_price = suppliers[:1].price
