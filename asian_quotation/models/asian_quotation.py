from odoo import models, fields, api


class AsianQuotation(models.Model):
    _name = 'asian.quotation'
    _description = 'Asian Quotation'

    name = fields.Char(string='Tiêu đề', required=True)
    vat = fields.Float(string='VAT (%)', default=0, help='Điền vào % VAT. Eg: 25')
    rate = fields.Float(string='Tỉ giá', default=23000)
    net_price = fields.Float(string='Giá NET SINGLE (USD)', compute='_compute_net_price')
    asian_spreadsheet_product_ids = fields.Many2many(string='Asian Spreadsheet Product', comodel_name='asian.spreadsheet.product', copy=False)
    asian_spreadsheet_option_ids = fields.One2many(string='Asian Spreadsheet Option', comodel_name='asian.spreadsheet.option', inverse_name='asian_quotation_id', copy=False)
    asian_spreadsheet_team_option_ids = fields.Many2many(string='Asian Spreadsheet Team Option', comodel_name='asian.spreadsheet.team.option', copy=False)
    asian_spreadsheet_net_option_ids = fields.Many2many(string='Asian Spreadsheet Net Option', comodel_name='asian.spreadsheet.net.option', copy=False)
    applied_asian_spreadsheet_option_id = fields.Many2one(string='Applied Asian Spreadsheet Option', comodel_name='asian.spreadsheet.option', compute='_compute_applied_asian_spreadsheet_option_id', copy=False)

    @api.depends('vat', 'rate', 'asian_spreadsheet_product_ids', 'asian_spreadsheet_product_ids.hotel_price')
    def _compute_net_price(self):
        for rec in self:
            hotel_price = sum(rec.asian_spreadsheet_product_ids.mapped('hotel_price')) / 2
            vat = 1 + max(0, rec.vat) / 100
            rec.net_price = (hotel_price * vat / rec.rate)

    @api.depends('asian_spreadsheet_option_ids.apply')
    def _compute_applied_asian_spreadsheet_option_id(self):
        for rec in self:
            option = rec.asian_spreadsheet_option_ids.filtered(lambda o: o.apply)[:1]
            rec.applied_asian_spreadsheet_option_id = option
            rec.asian_spreadsheet_product_ids = option.asian_spreadsheet_product_ids
            rec.asian_spreadsheet_team_option_ids = option.asian_spreadsheet_team_option_ids
            rec.asian_spreadsheet_net_option_ids = option.asian_spreadsheet_net_option_ids

    @api.model
    def _prepare_some_thing(self, values):
        team_option_result = []
        for val in values.get('asian_spreadsheet_team_option_ids', []):
            if len(val) == 3 and val[0] == 0:
                team_option_result.append(val[2])
        net_option_result = []
        for val in values.get('asian_spreadsheet_net_option_ids', []):
            if len(val) == 3 and val[0] == 0:
                net_option_result.append(val[2])
        product_result = []
        for val in values.get('asian_spreadsheet_product_ids', []):
            if len(val) == 3 and val[0] == 0:
                product_result.append(val[2])

        return team_option_result, net_option_result, product_result

    @api.multi
    def _update_some_thing(self, team_option_data, net_option_data, product_data):
        for rec in self:
            option = rec.asian_spreadsheet_option_ids.filtered(lambda o: o.apply)[:1]
            rec.asian_spreadsheet_product_ids.write({'asian_spreadsheet_option_id': option.id})
            team_option_to_update = option.asian_spreadsheet_team_option_ids
            for val in team_option_data:
                to_update = team_option_to_update[:1]
                to_update and to_update.write(val)
                team_option_to_update -= to_update

            net_option_to_update = option.asian_spreadsheet_net_option_ids
            for val in net_option_data:
                to_update = net_option_to_update[:1]
                to_update and to_update.write(val)
                net_option_to_update -= to_update

            product_to_update = option.asian_spreadsheet_product_ids
            for val in product_data:
                to_update = product_to_update[:1]
                to_update and to_update.write(val)
                product_to_update -= to_update

    @api.model
    def create(self, values):
        asian_spreadsheet_team_option_ids_list, asian_spreadsheet_net_option_ids_list, asian_spreadsheet_product_ids_list = self._prepare_some_thing(values)
        res = super(AsianQuotation, self).create(values)
        res._update_some_thing(asian_spreadsheet_team_option_ids_list, asian_spreadsheet_net_option_ids_list, asian_spreadsheet_product_ids_list)
        return res

    @api.multi
    def write(self, values):
        asian_spreadsheet_team_option_ids_list, asian_spreadsheet_net_option_ids_list, asian_spreadsheet_product_ids_list = self._prepare_some_thing(values)
        res = super(AsianQuotation, self).write(values)
        self._update_some_thing(asian_spreadsheet_team_option_ids_list, asian_spreadsheet_net_option_ids_list, asian_spreadsheet_product_ids_list)
        return res
