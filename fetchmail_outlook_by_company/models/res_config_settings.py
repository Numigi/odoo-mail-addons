# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/AGPL).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    microsoft_outlook_client_identifier_per_company = fields.Char(
        related='company_id.microsoft_outlook_client_identifier')
    microsoft_outlook_client_secret_per_company = fields.Char(
        related='company_id.microsoft_outlook_client_secret')
