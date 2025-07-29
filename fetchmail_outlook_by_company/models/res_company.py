# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/AGPL).

from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    microsoft_outlook_client_identifier = fields.Char(
        'Outlook Client Id')
    microsoft_outlook_client_secret = fields.Char(
        'Outlook Client Secret')
