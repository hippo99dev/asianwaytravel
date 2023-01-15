from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    show_brief_itinerary = fields.Boolean(default=True)
    show_schedule = fields.Boolean(default=True)
