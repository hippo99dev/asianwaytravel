from odoo import models, fields, api


class SaleOrderPaymentLine(models.Model):
    _inherit = 'sale.order.payment.line'

    payment_guider_id = fields.Many2one(string='Người thanh toán', comodel_name='res.partner')
    after_tour_type = fields.Selection(string='Loại', selection=[('hotel', 'Hotel')])
    after_tour_product_types = fields.Selection(
        string="Loại dịch vụ",
        selection=[
            ('hotel', 'Khách sạn'), ('meal', 'Nhà hàng'),
            ('transportation', 'Di chuyển'),
            ('plane_ticket', 'Vé máy bay/ Tàu hỏa'), ('ticket', 'Vé thắng cảnh'), ('guider', 'Hướng dẫn viên'),
            ('others', 'Dịch vụ khác'),
        ],
    )

    @api.model
    def create(self, values):
        res = super(SaleOrderPaymentLine, self).create(values)

        return res
