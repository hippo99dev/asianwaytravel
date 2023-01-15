from odoo import models, fields, api


class AsianQuotation(models.Model):
    _name = 'asian.quotation'
    _description = 'Asian Quotation'

    name = fields.Char(string='Tiêu đề', required=True)
    vat = fields.Float(string='VAT (%)', default=0, help='Điền vào % VAT. Eg: 25')
    rate = fields.Float(string='Tỉ giá', default=lambda self: self.env.ref('base.VND').rate)
    net_price = fields.Float(string='Giá NET SINGLE (USD)', compute='_compute_net_price')
    asian_quotation_schedule_ids = fields.Many2many(string='Asian Quotation Schedule', comodel_name='asian.quotation.schedule', copy=False)
    asian_spreadsheet_product_ids = fields.Many2many(string='Asian Spreadsheet Product', comodel_name='asian.spreadsheet.product', copy=False)
    asian_spreadsheet_option_ids = fields.One2many(string='Asian Spreadsheet Option', comodel_name='asian.spreadsheet.option', inverse_name='asian_quotation_id', copy=False)
    asian_spreadsheet_team_option_ids = fields.Many2many(string='Asian Spreadsheet Team Option', comodel_name='asian.spreadsheet.team.option', copy=False)
    asian_spreadsheet_net_option_ids = fields.Many2many(string='Asian Spreadsheet Net Option', comodel_name='asian.spreadsheet.net.option', copy=False)
    applied_asian_spreadsheet_option_id = fields.Many2one(string='Applied Asian Spreadsheet Option', comodel_name='asian.spreadsheet.option', compute='_compute_applied_asian_spreadsheet_option_id', copy=False)
    sale_order_ids = fields.One2many(string='Sale Order', comodel_name='sale.order', inverse_name='asian_quotation_id', copy=False)
    sale_order_count = fields.Integer(string='Sale Order Count', compute='_compute_sale_order_count')

    @api.depends('vat', 'rate', 'asian_spreadsheet_product_ids', 'asian_spreadsheet_product_ids.hotel_price')
    def _compute_net_price(self):
        for rec in self:
            hotel_price = sum(rec.asian_spreadsheet_product_ids.mapped('hotel_price')) / 2
            vat = 1 + max(0, rec.vat) / 100
            rec.net_price = (hotel_price * 1000 * vat / rec.rate)

    @api.depends('asian_spreadsheet_option_ids.apply')
    def _compute_applied_asian_spreadsheet_option_id(self):
        for rec in self:
            option = rec.asian_spreadsheet_option_ids.filtered(lambda o: o.apply)[:1]
            rec.applied_asian_spreadsheet_option_id = option
            rec.asian_quotation_schedule_ids = option.asian_quotation_schedule_ids
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
        schedule_result = []
        for val in values.get('asian_quotation_schedule_ids', []):
            if len(val) == 3 and val[0] == 0:
                schedule_result.append(val[2])

        return team_option_result, net_option_result, product_result, schedule_result

    @api.multi
    def _update_some_thing(self, team_option_data, net_option_data, product_data, schedule_data):
        for rec in self:
            option = rec.asian_spreadsheet_option_ids.filtered(lambda o: o.apply)[:1]
            rec.asian_quotation_schedule_ids.write({'asian_spreadsheet_option_id': option.id})
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

            schedule_to_update = option.asian_quotation_schedule_ids
            for val in schedule_data:
                to_update = schedule_to_update[:1]
                to_update and to_update.write(val)
                schedule_to_update -= to_update

    @api.model
    def create(self, values):
        asian_spreadsheet_team_option_ids_list, asian_spreadsheet_net_option_ids_list, asian_spreadsheet_product_ids_list, asian_quotation_schedule_ids_list = self._prepare_some_thing(values)
        res = super(AsianQuotation, self).create(values)
        res._update_some_thing(asian_spreadsheet_team_option_ids_list, asian_spreadsheet_net_option_ids_list, asian_spreadsheet_product_ids_list, asian_quotation_schedule_ids_list)
        return res

    @api.multi
    def write(self, values):
        asian_spreadsheet_team_option_ids_list, asian_spreadsheet_net_option_ids_list, asian_spreadsheet_product_ids_list, asian_quotation_schedule_ids_list = self._prepare_some_thing(values)
        res = super(AsianQuotation, self).write(values)
        self._update_some_thing(asian_spreadsheet_team_option_ids_list, asian_spreadsheet_net_option_ids_list, asian_spreadsheet_product_ids_list, asian_quotation_schedule_ids_list)
        return res

    @api.multi
    def action_create_sale_order(self):
        self.ensure_one()
        order = self.env['sale.order'].create({
            'partner_id': self.env.user.partner_id.id,
            'asian_quotation_id': self.id,
        })
        for line in self.asian_quotation_schedule_ids:
            self.env['sale.order.schedule'].create({
                'sale_order_id': order.id,
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
            })

        for line in self.asian_spreadsheet_product_ids:
            self.env['sale.order.sub.line'].create({
                'order_id': order.id,
                'product_types': 'hotel',
                'product_id': line.hotel_id.id,
                'date_checkin': fields.Date.today(),
                'date_checkout': fields.Date.today(),
            })

        return {
            'name': 'Đơn hàng',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': order.id,
            'res_model': 'sale.order',
            'view_id': self.env.ref('sale.view_order_form').id,
            'context': dict(create=False),
            'target': 'current',
        }

    @api.depends('sale_order_ids')
    def _compute_sale_order_count(self):
        for rec in self:
            rec.sale_order_count = len(rec.sale_order_ids)

    def action_view_sale_order(self):
        self.ensure_one()
        action = self.env.ref('sale.action_quotations_with_onboarding')
        action = action and action.read()[0]
        action['domain'] = [('id', 'in', self.sale_order_ids.ids)]
        return action
