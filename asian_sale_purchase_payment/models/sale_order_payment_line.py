from odoo import models, fields, api


class SaleOrderPaymentLine(models.Model):
    _inherit = 'sale.order.payment.line'

    payment_guider_id = fields.Many2one(string='Người thanh toán', comodel_name='res.partner')
