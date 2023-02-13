from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    show_brief_itinerary = fields.Boolean(default=True)
    show_schedule = fields.Boolean(default=True)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(SaleOrder, self).fields_view_get(view_id, view_type, toolbar, submenu)

        if self.env.ref('sale.action_quotations_with_onboarding').id == self._context.get('params', {}).get('action'):
            prints = result.get('toolbar', {}).get('print', {})
            if prints:
                new_prints = []
                for p in prints:
                    if p.get('xml_id') == 'asia_sale.asia_sale_order_report_quatation_customer_docx':
                        continue
                    new_prints.append(p)
                result['toolbar']['print'] = new_prints

            actions = result.get('toolbar', {}).get('action', {})
            if actions:
                new_actions = []
                for act in actions:
                    if act.get('xml_id') in ('asia_sale.asia_sale_guider_print', 'asia_sale.guider_contract_print'):
                        continue
                    new_actions.append(act)
                result['toolbar']['action'] = new_actions

        return result
