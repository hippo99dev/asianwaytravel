from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    is_guider = fields.Boolean(string='Is Guide', compute='_compute_is_guider')

    @api.multi
    def _compute_is_guider(self):
        for rec in self:
            rec.is_guider = bool(self.env.user.partner_id.service_type.filtered(lambda o: o.tag_type == 'guider'))

    def action_view_sale_order_payment(self):
        self.ensure_one()
        action = self.env.ref('asian_sale_purchase_payment.sale_order_payment__act_window')
        action = action and action.read()[0]
        action['domain'] = [('id', 'in', self.order_id.payment_ids.ids)]
        return action

    def action_view_sale_order_payment_tour_report(self):
        self.ensure_one()
        action = self.env.ref('asian_sale_purchase_payment.sale_order_payment__tour_report__act_window')
        action = action and action.read()[0]
        action['domain'] = [('id', 'in', self.order_id.payment_ids.ids)]
        return action

    def export_sale_order_guider(self):
        self.ensure_one()
        return {
            'name': 'In cho hướng dẫn viên',
            'view_mode': 'form',
            'res_model': 'sale.report.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_order_id': self.order_id.id, 'default_type': 'guider', 'active_id': self.order_id.id, 'active_ids': self.order_id.ids}
        }

    def export_contract_guider(self):
        self.ensure_one()
        return {
            'name': 'Hợp đồng HDV',
            'view_mode': 'form',
            'res_model': 'guider.contract.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_order_id': self.order_id.id}
        }
