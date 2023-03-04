from odoo import models, fields, api
from odoo.osv import expression


class AsianSpreadsheetProduct(models.Model):
    _name = 'asian.spreadsheet.product'
    _description = 'Asian Spreadsheet Product'
    _rec_name = 'date_number'
    _order = 'sequence, date_number'

    date_number = fields.Char('Date')
    travel_itinerary = fields.Text('Itinarary')
    vendor_id = fields.Many2one('res.partner', string="Nhà cung cấp", domain=[('is_hotel', '=', True)])
    hotel_price = fields.Float(string='Hotel Price')
    # hotel_price = fields.Float(string='Giá khách sạn', compute='_compute_hotel_price', store=True)
    hotel_id = fields.Many2one(string='Hotel', comodel_name='product.product', domain=[('product_types', '=', 'hotel')])
    meal_price = fields.Float(string='Restaurant')
    ticket_price = fields.Float(string='Entrance fee')
    show_price = fields.Float(string='Service + Show')
    transit_price = fields.Float(string='Transport (Km)', help='Điền vào Km. Eg: 10')
    transport_price = fields.Float(string='Group fee')
    guide_price = fields.Float(string='Guide')
    note = fields.Text(string='Note')

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
                rec.hotel_price = suppliers[:1].price / 1000

    @api.onchange('vendor_id', 'hotel_id')
    def _onchange_vendor_id(self):
        product_id_domain = [('product_types', '=', 'hotel')]
        if self.vendor_id:
            product_id_domain += [('vendor_id', '=', self.vendor_id.id)]
        if self.hotel_id:
            self.vendor_id = self.hotel_id.vendor_id
        return {'domain': {'hotel_id': product_id_domain}}
