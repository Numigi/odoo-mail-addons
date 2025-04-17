# mail_template_archive/models/mail_template.py
# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


class MailTemplate(models.Model):
    """Add active field to mail templates to allow archiving."""
    
    _inherit = 'mail.template'

    active = fields.Boolean(
        string='Active',
        default=True,
        help="If unchecked, it will allow you to hide the email template without removing it.",
    )
    
    @api.multi
    def action_archive(self):
        """Archive the selected mail templates."""
        self.write({'active': False})
        return True
        
    @api.multi
    def action_unarchive(self):
        """Unarchive the selected mail templates."""
        self.write({'active': True})
        return True
