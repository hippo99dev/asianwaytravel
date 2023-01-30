from odoo import models, fields


class DefaultVehiclePrice(models.Model):
    _name = 'default.vehicle.price'
    _description = 'DefaultVehiclePrice'

    name = fields.Char(string='Loại xe')
    price = fields.Float(string='Giá')
