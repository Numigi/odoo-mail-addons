# Copyright 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from odoo import models, fields


class MailTemplate(models.Model):
    """Add active field to mail templates to allow archiving."""
    
    _inherit = 'mail.template'

    active = fields.Boolean(
        string='Active',
        default=True,
        help="If unchecked, it will allow you to hide the email template without removing it.",
    )
