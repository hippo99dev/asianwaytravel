from odoo import models, fields, api


class SaleOrderPayment(models.Model):
    _inherit = 'sale.order.payment'

    is_guider = fields.Boolean(string='Is Guide', compute='_compute_is_guider')
    incurred_cost_payment_line_ids = fields.One2many('incurred.cost.payment_line', "payment_id", string="Phát sinh")

    @api.multi
    def _compute_is_guider(self):
        for rec in self:
            rec.is_guider = bool(self.env.user.partner_id.service_type.filtered(lambda o: o.tag_type == 'guider'))
