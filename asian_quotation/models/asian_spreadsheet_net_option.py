from odoo import models, fields, api


class AsianSpreadsheetNetOption(models.Model):
    _name = 'asian.spreadsheet.net.option'
    _description = 'Asian Spreadsheet Net Option'

    name = fields.Char(string='Loại giá')
    profit = fields.Float(string='Lợi nhuận')
    car_4 = fields.Float(string='2 khách', compute='_compute_car_x')
    car_7 = fields.Float(string='3 khách', compute='_compute_car_x')
    car_16 = fields.Float(string='6 khách', compute='_compute_car_x')
    car_29 = fields.Float(string='10 khách', compute='_compute_car_x')
    car_35 = fields.Float(string='15 khách', compute='_compute_car_x')
    car_45_1 = fields.Float(string='20 khách', compute='_compute_car_x')
    car_45_2 = fields.Float(string='25 khách', compute='_compute_car_x')
    car_45_3 = fields.Float(string='30 khách', compute='_compute_car_x')
    car_45_4 = fields.Float(string='35 khách', compute='_compute_car_x')
    apply = fields.Boolean(string='Tính báo giá')
    type_line = fields.Selection(string='Type Line', selection=[('net', 'Giá NET/khách'), ('net_usd', 'GIÁ NET USD')])
    asian_spreadsheet_option_id = fields.Many2one(string='Asian Spreadsheet Option', comodel_name='asian.spreadsheet.option', ondelete='cascade')
    asian_quotation_id = fields.Many2one(string='Asian Quotation', comodel_name='asian.quotation')

    @api.depends(
        'asian_quotation_id.asian_spreadsheet_product_ids',
        'asian_quotation_id.asian_spreadsheet_product_ids.hotel_price',
        'asian_quotation_id.asian_spreadsheet_product_ids.meal_price',
        'asian_quotation_id.asian_spreadsheet_product_ids.ticket_price',
        'asian_quotation_id.asian_spreadsheet_product_ids.show_price',
        'asian_quotation_id.asian_spreadsheet_product_ids.transit_price',
        'asian_quotation_id.asian_spreadsheet_product_ids.transport_price',
        'asian_quotation_id.asian_spreadsheet_product_ids.guide_price',

        'asian_quotation_id.asian_spreadsheet_team_option_ids.car_4',
        'asian_quotation_id.asian_spreadsheet_team_option_ids.car_7',
        'asian_quotation_id.asian_spreadsheet_team_option_ids.car_16',
        'asian_quotation_id.asian_spreadsheet_team_option_ids.car_29',
        'asian_quotation_id.asian_spreadsheet_team_option_ids.car_35',
        'asian_quotation_id.asian_spreadsheet_team_option_ids.car_45_1',
        'asian_quotation_id.asian_spreadsheet_team_option_ids.car_45_2',
        'asian_quotation_id.asian_spreadsheet_team_option_ids.car_45_3',
    )
    def _compute_car_x(self):
        def calc_car_x(x):
            result = 0
            by_type_line_value = getattr(by_type_line, f'car_{x}') * 1000
            by_team_line_value = getattr(by_team_line, f'car_{x}') * 1000
            if by_team_line_value:
                result = own_expenses + (general_expenses + transit_price * by_type_line_value) / by_team_line_value

            return result

        for rec in self:
            hotel_price = meal_price = ticket_price = show_price = transit_price = transport_price = guide_price = 0
            for line in rec.asian_spreadsheet_option_id.asian_spreadsheet_product_ids:
                hotel_price += line.hotel_price * 1000
                meal_price += line.meal_price * 1000
                ticket_price += line.ticket_price * 1000
                show_price += line.show_price * 1000

                transit_price += line.transit_price
                transport_price += line.transport_price * 1000
                guide_price += line.guide_price * 1000
            own_expenses = hotel_price / 2 + meal_price + ticket_price + show_price
            general_expenses = transport_price + guide_price

            by_type_line = rec.asian_spreadsheet_option_id.asian_spreadsheet_team_option_ids.filtered(lambda o: o.type_line == 'by_type')
            by_team_line = rec.asian_spreadsheet_option_id.asian_spreadsheet_team_option_ids.filtered(lambda o: o.type_line == 'by_team')

            car_4 = calc_car_x('4')
            car_7 = calc_car_x('7')
            car_16 = calc_car_x('16')
            car_29 = calc_car_x('29')
            car_35 = calc_car_x('35')
            car_45_1 = calc_car_x('45_1')
            car_45_2 = calc_car_x('45_2')
            car_45_3 = calc_car_x('45_3')
            car_45_4 = calc_car_x('45_4')
            
            rate = rec.asian_quotation_id.rate
            if rec.type_line == 'net_usd' and rate:
                car_4 = max(car_4 / rate, 0)
                car_7 = max(car_7 / rate, 0)
                car_16 = max(car_16 / rate, 0)
                car_29 = max(car_29 / rate, 0)
                car_35 = max(car_35 / rate, 0)
                car_45_1 = max(car_45_1 / rate, 0)
                car_45_2 = max(car_45_2 / rate, 0)
                car_45_3 = max(car_45_3 / rate, 0)
                car_45_4 = max(car_45_4 / rate, 0)

            rec.car_4 = car_4
            rec.car_7 = car_7
            rec.car_16 = car_16
            rec.car_29 = car_29
            rec.car_35 = car_35
            rec.car_45_1 = car_45_1
            rec.car_45_2 = car_45_2
            rec.car_45_3 = car_45_3
            rec.car_45_4 = car_45_4
