from odoo import api, models, fields


class EditorInformationWizard(models.TransientModel):
    _inherit = 'editor.information.wizard'

    name = fields.Char(string='Người đăng nhập')
