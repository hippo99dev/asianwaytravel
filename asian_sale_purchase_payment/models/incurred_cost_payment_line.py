from odoo import models, fields, api


class IncurredCostPaymentLine(models.Model):
    _name = 'incurred.cost.payment_line'
    _description = 'Incurred Cost Payment Line'

    payment_id = fields.Many2one('sale.order.payment', ondelete='cascade')
    date_checkin = fields.Date(string="Checkin")
    date_checkout = fields.Date(string="Checkout")
    product_id = fields.Many2one(comodel_name="product.product", string="Dich vụ")
    currency_id = fields.Many2one('res.currency', related='payment_id.currency_id')
    vendor_id = fields.Many2one('res.partner', related="product_id.vendor_id", string="Nhà Cung Cấp")
    foc = fields.Float(string="FOC")
    product_uom_qty = fields.Float(string='Số lượng')
    allotment_use = fields.Float(string="Allotment sử dụng")
    nite = fields.Float(string="Số đêm", compute='_compute_nite', store=True)
    price_subtotal = fields.Monetary(string='Thành tiền', compute='_compute_price_subtotal')
    extra_fee = fields.Monetary(string='Phát sinh')
    note = fields.Text(string='Ghi chú')
    meal = fields.Selection(string='Bữa ăn', selection=[
        ('breakfast', 'Breakfast'),
        ('brunch', 'Brunch'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('other', 'Other'),
    ])
    date_line = fields.Date('Ngày')
    price_unit = fields.Float('Đơn giá')
    payment_method = fields.Selection([('bank', 'Chuyển khoản'), ('bank_by_day', 'Chuyển khoản theo ngày'), ('cash', 'Tiền mặt'), ('credit', 'Công nợ')], string='Hình thức thanh toán')
    payment_date = fields.Date('Hạn thanh toán')
    product_qty_changed = fields.Float('SL thay đổi')
    price_unit_changed = fields.Float('ĐG thay đổi')
    price_subtotal_changed = fields.Float('TT thay đổi')

    @api.depends('date_checkin', 'date_checkout')
    def _compute_nite(self):
        for rec in self:
            days = rec.date_checkout and rec.date_checkin and (rec.date_checkout - rec.date_checkin).days or 0
            rec.nite = max(1, days)

    @api.depends('product_uom_qty', 'price_unit')
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.product_uom_qty * rec.price_unit
