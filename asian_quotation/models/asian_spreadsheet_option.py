from odoo import models, fields, api, exceptions


class AsianSpreadsheetOption(models.Model):
    _name = 'asian.spreadsheet.option'
    _description = 'Asian Spreadsheet Option'

    name = fields.Char(string='Option')
    profit = fields.Float(string='Lợi nhuận', help='Điền vào lợi nhuận. Eg: 100.000')
    percent_profit = fields.Float(string='Lợi nhuận (%)', help='Điền vào % lợi nhuận. Eg: 25')
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
    is_selected = fields.Boolean(string='Đã tạo Tour', compute='_compute_is_selected', store=True)
    asian_quotation_id = fields.Many2one(string='Asian Quotation', comodel_name='asian.quotation', ondelete='cascade')
    asian_quotation_schedule_ids = fields.One2many(string='Asian Quotation Schedule', comodel_name='asian.quotation.schedule', inverse_name='asian_spreadsheet_option_id')
    asian_spreadsheet_product_ids = fields.One2many(string='Asian Spreadsheet Product', comodel_name='asian.spreadsheet.product', inverse_name='asian_spreadsheet_option_id')
    asian_spreadsheet_team_option_ids = fields.One2many(string='Asian Spreadsheet Team Option', comodel_name='asian.spreadsheet.team.option', inverse_name='asian_spreadsheet_option_id')
    asian_spreadsheet_net_option_ids = fields.One2many(string='Asian Spreadsheet Net Option', comodel_name='asian.spreadsheet.net.option', inverse_name='asian_spreadsheet_option_id')
    template_option_id = fields.Many2one(string='Template Option', comodel_name='asian.spreadsheet.option', domain="[('asian_quotation_id', '=', asian_quotation_id), ('id', '!=', id)]")

    @api.onchange('apply')
    def onchange_apply(self):
        if len(self.asian_quotation_id.asian_spreadsheet_option_ids.filtered(lambda o: o.apply)) > 2:
            raise exceptions.ValidationError("Không thể tính báo giá nhiều dòng!")

    def create_quotation_schedule(self):
        self.ensure_one()
        for line in self.asian_quotation_id.asian_quotation_schedule_ids:
            self.env['asian.quotation.schedule'].create({
                'sequence': line.sequence,
                'schedule_date': line.schedule_date,
                'schedule_act': line.schedule_act,
                'note': line.note,
                'customer_market': line.customer_market,
                'validate_season': line.validate_season,
                'meal_supplied': line.meal_supplied,
                'schedule_date_date': line.schedule_date_date,
                'weekday': line.weekday,
                'meal_ids': [(6, 0, line.meal_ids.ids)],
                'template_id': line.template_id,
                'asian_spreadsheet_option_id': self.id,
                'asian_quotation_id': self.asian_quotation_id.id,
            })

    def create_spreadsheet_product(self):
        self.ensure_one()
        for line in self.asian_quotation_id.asian_spreadsheet_product_ids:
            self.env['asian.spreadsheet.product'].create({
                'date_number': line.date_number,
                'travel_itinerary': line.travel_itinerary,
                'hotel_price': line.hotel_price,
                'meal_price': line.meal_price,
                'ticket_price': line.ticket_price,
                'show_price': line.show_price,
                'transit_price': line.transit_price,
                'transport_price': line.transport_price,
                'guide_price': line.guide_price,
                'asian_spreadsheet_option_id': self.id,
                'asian_quotation_id': self.asian_quotation_id.id,
            })

    def create_team_option(self):
        self.ensure_one()

        by_type = self.env['asian.spreadsheet.team.option'].create({
            'name': 'Giá theo loại xe/KM',
            'apply': True,
            'type_line': 'by_type',
            'asian_spreadsheet_option_id': self.id,
            'asian_quotation_id': self.asian_quotation_id.id,
            'car_4': self.asian_quotation_id.price_type_car_4 or self.env.ref('asian_quotation.car_4').price,
            'car_7': self.asian_quotation_id.price_type_car_7 or self.env.ref('asian_quotation.car_7').price,
            'car_16': self.asian_quotation_id.price_type_car_16 or self.env.ref('asian_quotation.car_16').price,
            'car_29': self.asian_quotation_id.price_type_car_29 or self.env.ref('asian_quotation.car_29').price,
            'car_35': self.asian_quotation_id.price_type_car_35 or self.env.ref('asian_quotation.car_35').price,
            'car_45_1': self.asian_quotation_id.price_type_car_45_1 or self.env.ref('asian_quotation.car_45_1').price,
            'car_45_2': self.asian_quotation_id.price_type_car_45_2 or self.env.ref('asian_quotation.car_45_2').price,
            'car_45_3': self.asian_quotation_id.price_type_car_45_3 or self.env.ref('asian_quotation.car_45_3').price,
            'car_45_4': self.asian_quotation_id.price_type_car_45_4 or self.env.ref('asian_quotation.car_45_4').price,
        })

        by_team = self.env['asian.spreadsheet.team.option'].create({
            'name': 'Nhóm khách',
            'apply': True,
            'type_line': 'by_team',
            'asian_spreadsheet_option_id': self.id,
            'asian_quotation_id': self.asian_quotation_id.id,
            'car_4': 2,
            'car_7': 3,
            'car_16': 6,
            'car_29': 10,
            'car_35': 15,
            'car_45_1': 20,
            'car_45_2': 25,
            'car_45_3': 30,
            'car_45_4': 35,
        })
        return True

    def create_net_option(self):
        net = self.env['asian.spreadsheet.net.option'].create({
            'name': 'Giá NET/khách',
            'apply': True,
            'type_line': 'net',
            'asian_spreadsheet_option_id': self.id,
            'asian_quotation_id': self.asian_quotation_id.id,
        })
        net_usd = self.env['asian.spreadsheet.net.option'].create({
            'name': 'GIÁ NET USD',
            'apply': True,
            'type_line': 'net_usd',
            'asian_spreadsheet_option_id': self.id,
            'asian_quotation_id': self.asian_quotation_id.id,
        })
        return True

    @api.model
    def create(self, values):
        res = super(AsianSpreadsheetOption, self).create(values)
        if res.apply:
            res.create_quotation_schedule()
            res.create_spreadsheet_product()
            res.create_team_option()
            res.create_net_option()
        # by_type = self.env['asian.spreadsheet.team.option'].create({
        #     'name': 'Giá theo loại xe/KM',
        #     'apply': True,
        #     'type_line': 'by_type',
        #     'asian_spreadsheet_option_id': res.id,
        #     'asian_quotation_id': res.asian_quotation_id.id,
        #     'car_4': self.env.ref('asian_quotation.car_4').price,
        #     'car_7': self.env.ref('asian_quotation.car_7').price,
        #     'car_16': self.env.ref('asian_quotation.car_16').price,
        #     'car_29': self.env.ref('asian_quotation.car_29').price,
        #     'car_35': self.env.ref('asian_quotation.car_35').price,
        #     'car_45_1': self.env.ref('asian_quotation.car_45_1').price,
        #     'car_45_2': self.env.ref('asian_quotation.car_45_2').price,
        #     'car_45_3': self.env.ref('asian_quotation.car_45_3').price,
        #     'car_45_4': self.env.ref('asian_quotation.car_45_4').price,
        # })

        # by_team = self.env['asian.spreadsheet.team.option'].create({
        #     'name': 'Nhóm khách',
        #     'apply': True,
        #     'type_line': 'by_team',
        #     'asian_spreadsheet_option_id': res.id,
        #     'asian_quotation_id': res.asian_quotation_id.id,
        #     'car_4': 2,
        #     'car_7': 3,
        #     'car_16': 6,
        #     'car_29': 10,
        #     'car_35': 15,
        #     'car_45_1': 20,
        #     'car_45_2': 25,
        #     'car_45_3': 30,
        #     'car_45_4': 35,
        # })
        # net = self.env['asian.spreadsheet.net.option'].create({
        #     'name': 'Giá NET/khách',
        #     'apply': True,
        #     'type_line': 'net',
        #     'asian_spreadsheet_option_id': res.id,
        #     'asian_quotation_id': res.asian_quotation_id.id,
        # })
        # net_usd = self.env['asian.spreadsheet.net.option'].create({
        #     'name': 'GIÁ NET USD',
        #     'apply': True,
        #     'type_line': 'net_usd',
        #     'asian_spreadsheet_option_id': res.id,
        #     'asian_quotation_id': res.asian_quotation_id.id,
        # })
        # if res.apply:
        #     res.asian_quotation_id._compute_applied_asian_spreadsheet_option_id()

        # res.asian_quotation_id.write({
        #     'asian_spreadsheet_team_option_ids': [(6, 0, [by_type.id, by_team.id])],
        #     'asian_spreadsheet_net_option_ids': [(6, 0, [net.id, net_usd.id])],
        # })

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

    def write(self, values):
        res = super(AsianSpreadsheetOption, self).write(values)
        if 'apply' in values and values.get('apply'):
            apply_line = self.filtered(lambda o: o.apply)[:1]
            if apply_line and not apply_line.asian_spreadsheet_team_option_ids:
                apply_line.create_team_option()
            if apply_line and not apply_line.asian_spreadsheet_net_option_ids:
                apply_line.create_net_option()
        return res

    @api.depends(
        'profit',
        'asian_quotation_id.asian_spreadsheet_net_option_ids.car_4',
    )
    def _compute_car_x(self):
        def calc_car_x(x):
            net_usd_line_value = getattr(net_usd_line, f'car_{x}')
            return net_usd_line_value * (100 + rec.percent_profit) / 100 + rec.profit

        for rec in self:
            # net_line = rec.asian_quotation_id.asian_spreadsheet_net_option_ids.filtered(lambda o: o.type_line == 'net')
            net_usd_line = rec.asian_spreadsheet_net_option_ids.filtered(lambda o: o.type_line == 'net_usd')

            rec.car_4 = calc_car_x('4')
            rec.car_7 = calc_car_x('7')
            rec.car_16 = calc_car_x('16')
            rec.car_29 = calc_car_x('29')
            rec.car_35 = calc_car_x('35')
            rec.car_45_1 = calc_car_x('45_1')
            rec.car_45_2 = calc_car_x('45_2')
            rec.car_45_3 = calc_car_x('45_3')
            rec.car_45_4 = calc_car_x('45_4')

    def action_copy_option(self):
        asian_quotation_schedule_ids = [(5, 0, 0)]
        asian_spreadsheet_product_ids = [(5, 0, 0)]
        asian_spreadsheet_team_option_ids = [(5, 0, 0)]
        asian_spreadsheet_net_option_ids = [(5, 0, 0)]
        for line in self.template_option_id.asian_quotation_schedule_ids:
            asian_quotation_schedule_ids.append(
                (0, 0, {
                    'sequence': line.sequence,
                    'schedule_date': line.schedule_date,
                    'schedule_act': line.schedule_act,
                    'note': line.note,
                    'customer_market': line.customer_market,
                    'validate_season': line.validate_season,
                    'meal_supplied': line.meal_supplied,
                    'schedule_date_date': line.schedule_date_date,
                    'weekday': line.weekday,
                    'meal_ids': [(6, 0, line.meal_ids.ids)],
                    'asian_spreadsheet_option_id': self.id,
                })
            )

        for line in self.template_option_id.asian_spreadsheet_product_ids:
            asian_spreadsheet_product_ids.append(
                (0, 0, {
                    'date_number': line.date_number,
                    'travel_itinerary': line.travel_itinerary,
                    'hotel_price': line.hotel_price,
                    'hotel_id': line.hotel_id.id,
                    'meal_price': line.meal_price,
                    'ticket_price': line.ticket_price,
                    'show_price': line.show_price,
                    'transit_price': line.transit_price,
                    'transport_price': line.transport_price,
                    'guide_price': line.guide_price,
                    'sequence': line.sequence,
                    'type_line': line.type_line,
                    'asian_quotation_id': line.asian_quotation_id.id,
                    'asian_spreadsheet_option_id': self.id,
                })
            )

        for line in self.template_option_id.asian_spreadsheet_team_option_ids:
            asian_spreadsheet_team_option_ids.append(
                (0, 0, {
                    'name': line.name,
                    'profit': line.profit,
                    'car_4': line.car_4,
                    'car_7': line.car_7,
                    'car_16': line.car_16,
                    'car_29': line.car_29,
                    'car_35': line.car_35,
                    'car_45_1': line.car_45_1,
                    'car_45_2': line.car_45_2,
                    'car_45_3': line.car_45_3,
                    'car_45_4': line.car_45_4,
                    'apply': line.apply,
                    'type_line': line.type_line,
                    'asian_quotation_id': line.asian_quotation_id.id,
                    'asian_spreadsheet_option_id': self.id,
                })
            )

        for line in self.template_option_id.asian_spreadsheet_net_option_ids:
            asian_spreadsheet_net_option_ids.append(
                (0, 0, {
                    'name': line.name,
                    'profit': line.profit,
                    'car_4': line.car_4,
                    'car_7': line.car_7,
                    'car_16': line.car_16,
                    'car_29': line.car_29,
                    'car_35': line.car_35,
                    'car_45_1': line.car_45_1,
                    'car_45_2': line.car_45_2,
                    'car_45_3': line.car_45_3,
                    'car_45_4': line.car_45_4,
                    'apply': line.apply,
                    'type_line': line.type_line,
                    'asian_quotation_id': line.asian_quotation_id.id,
                    'asian_spreadsheet_option_id': self.id,
                })
            )
        self.write({
            'asian_quotation_schedule_ids': asian_quotation_schedule_ids,
            'asian_spreadsheet_product_ids': asian_spreadsheet_product_ids,
            'asian_spreadsheet_team_option_ids': asian_spreadsheet_team_option_ids,
            'asian_spreadsheet_net_option_ids': asian_spreadsheet_net_option_ids,
        })

    @api.depends('asian_quotation_id.sale_order_ids', 'asian_quotation_id.sale_order_ids.state')
    def _compute_is_selected(self):
        for rec in self:
            rec.is_selected = bool(rec.asian_quotation_id.sale_order_ids.filtered(lambda o: o.state != 'cancel' and o.asian_spreadsheet_option_id.id == rec.id))
