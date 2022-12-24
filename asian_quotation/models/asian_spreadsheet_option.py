from odoo import models, fields, api, exceptions


class AsianSpreadsheetOption(models.Model):
    _name = 'asian.spreadsheet.option'
    _description = 'Asian Spreadsheet Option'

    name = fields.Char(string='Option')
    profit = fields.Float(string='Lợi nhuận (%)', help='Điền vào % lợi nhuận. Eg: 25')
    car_4 = fields.Float(string='Xe 4 chỗ', compute='_compute_car_x')
    car_7 = fields.Float(string='Xe 7 chỗ', compute='_compute_car_x')
    car_16 = fields.Float(string='Xe 16 chỗ', compute='_compute_car_x')
    car_29 = fields.Float(string='Xe 29 chỗ', compute='_compute_car_x')
    car_35 = fields.Float(string='Xe 35 chỗ', compute='_compute_car_x')
    car_45_1 = fields.Float(string='Xe 45 chỗ', compute='_compute_car_x')
    car_45_2 = fields.Float(string='Xe 45 chỗ', compute='_compute_car_x')
    car_45_3 = fields.Float(string='Xe 45 chỗ', compute='_compute_car_x')
    car_45_4 = fields.Float(string='Xe 45 chỗ', compute='_compute_car_x')
    apply = fields.Boolean(string='Tính báo giá')
    asian_quotation_id = fields.Many2one(string='Asian Quotation', comodel_name='asian.quotation', ondelete='cascade')
    asian_spreadsheet_product_ids = fields.One2many(string='Asian Spreadsheet Product', comodel_name='asian.spreadsheet.product', inverse_name='asian_spreadsheet_option_id')
    asian_spreadsheet_team_option_ids = fields.One2many(string='Asian Spreadsheet Team Option', comodel_name='asian.spreadsheet.team.option', inverse_name='asian_spreadsheet_option_id')
    asian_spreadsheet_net_option_ids = fields.One2many(string='Asian Spreadsheet Net Option', comodel_name='asian.spreadsheet.net.option', inverse_name='asian_spreadsheet_option_id')

    @api.onchange('apply')
    def onchange_apply(self):
        if len(self.asian_quotation_id.asian_spreadsheet_option_ids.filtered(lambda o: o.apply)) > 2:
            raise exceptions.ValidationError("Không thể tính báo giá nhiều dòng!")

    @api.model
    def create(self, values):
        res = super(AsianSpreadsheetOption, self).create(values)
        by_type = self.env['asian.spreadsheet.team.option'].create({
            'name': 'Giá theo loại xe/KM',
            'apply': True,
            'type_line': 'by_type',
            'asian_spreadsheet_option_id': res.id,
            'asian_quotation_id': res.asian_quotation_id.id,
        })
        by_team = self.env['asian.spreadsheet.team.option'].create({
            'name': 'Nhóm khách',
            'apply': True,
            'type_line': 'by_team',
            'asian_spreadsheet_option_id': res.id,
            'asian_quotation_id': res.asian_quotation_id.id,
        })
        net = self.env['asian.spreadsheet.net.option'].create({
            'name': 'Giá NET/khách',
            'apply': True,
            'type_line': 'net',
            'asian_spreadsheet_option_id': res.id,
            'asian_quotation_id': res.asian_quotation_id.id,
        })
        net_usd = self.env['asian.spreadsheet.net.option'].create({
            'name': 'GIÁ NET USD',
            'apply': True,
            'type_line': 'net_usd',
            'asian_spreadsheet_option_id': res.id,
            'asian_quotation_id': res.asian_quotation_id.id,
        })

        # for val in [
        #     {
        #         'date_number': '11Mar',
        #         'travel_itinerary': 'Hanoi',
        #         'hotel_price': 850000,
        #         'meal_price': 0,
        #         'ticket_price': 0,
        #         'show_price': 35000,
        #         'transit_price': 200,
        #         'transport_price': 0,
        #         'guide_price': 600000,
        #         'asian_spreadsheet_option_id': res.id,
        #         'asian_quotation_id': res.asian_quotation_id.id,
        #     },
        #     {
        #         'date_number': '12Mar',
        #         'travel_itinerary': 'Ninh Binh- Hanoi',
        #         'hotel_price': 750000,
        #         'meal_price': 200000,
        #         'ticket_price': 310000,
        #         'show_price': 0,
        #         'transit_price': 320,
        #         'transport_price': 60000,
        #         'guide_price': 600000,
        #         'asian_spreadsheet_option_id': res.id,
        #         'asian_quotation_id': res.asian_quotation_id.id,
        #     },
        #     {
        #         'date_number': '13Mar',
        #         'travel_itinerary': 'Hanoi- Halong',
        #         'hotel_price': 560000,
        #         'meal_price': 0,
        #         'ticket_price': 0,
        #         'show_price': 0,
        #         'transit_price': 250,
        #         'transport_price': 200000,
        #         'guide_price': 600000,
        #         'asian_spreadsheet_option_id': res.id,
        #         'asian_quotation_id': res.asian_quotation_id.id,
        #     },
        #     {
        #         'date_number': '14Mar',
        #         'travel_itinerary': 'Halong- Hanoi',
        #         'hotel_price': 750000,
        #         'meal_price': 0,
        #         'ticket_price': 0,
        #         'show_price': 0,
        #         'transit_price': 250,
        #         'transport_price': 0,
        #         'guide_price': 600000,
        #         'asian_spreadsheet_option_id': res.id,
        #         'asian_quotation_id': res.asian_quotation_id.id,
        #     },
        #     {
        #         'date_number': '15Mar',
        #         'travel_itinerary': 'Hanoi- Sai gon',
        #         'hotel_price': 700000,
        #         'meal_price': 0,
        #         'ticket_price': 0,
        #         'show_price': 0,
        #         'transit_price': 200,
        #         'transport_price': 0,
        #         'guide_price': 1200000,
        #         'asian_spreadsheet_option_id': res.id,
        #         'asian_quotation_id': res.asian_quotation_id.id,
        #     },
        #     {
        #         'date_number': '16Mar',
        #         'travel_itinerary': 'SAi gon tự do',
        #         'hotel_price': 250000,
        #         'meal_price': 0,
        #         'ticket_price': 0,
        #         'show_price': 0,
        #         'transit_price': 0,
        #         'transport_price': 0,
        #         'guide_price': 0,
        #         'asian_spreadsheet_option_id': res.id,
        #         'asian_quotation_id': res.asian_quotation_id.id,
        #     },
        #     {
        #         'date_number': '18Mar',
        #         'travel_itinerary': 'Tiễn sân bay',
        #         'hotel_price': 850000,
        #         'meal_price': 0,
        #         'ticket_price': 0,
        #         'show_price': 0,
        #         'transit_price': 100,
        #         'transport_price': 0,
        #         'guide_price': 600000,
        #         'asian_spreadsheet_option_id': res.id,
        #         'asian_quotation_id': res.asian_quotation_id.id,
        #     },
        # ]:
        #     self.env['asian.spreadsheet.product'].create(val)

        return res

    @api.depends(
        'profit',
        'asian_quotation_id.asian_spreadsheet_net_option_ids.car_4',
    )
    def _compute_car_x(self):
        def calc_car_x(x):
            net_usd_line_value = getattr(net_usd_line, f'car_{x}')
            return net_usd_line_value * (100 + rec.profit) / 100 + net_line.profit

        for rec in self:
            net_line = rec.asian_quotation_id.asian_spreadsheet_net_option_ids.filtered(lambda o: o.type_line == 'net')
            net_usd_line = rec.asian_quotation_id.asian_spreadsheet_net_option_ids.filtered(lambda o: o.type_line == 'net_usd')

            rec.car_4 = calc_car_x('4')
            rec.car_7 = calc_car_x('7')
            rec.car_16 = calc_car_x('16')
            rec.car_29 = calc_car_x('29')
            rec.car_35 = calc_car_x('35')
            rec.car_45_1 = calc_car_x('45_1')
            rec.car_45_2 = calc_car_x('45_2')
            rec.car_45_3 = calc_car_x('45_3')
            rec.car_45_4 = calc_car_x('45_4')
