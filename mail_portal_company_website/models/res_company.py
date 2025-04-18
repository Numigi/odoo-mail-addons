# © 2025 Numigi
# License LGPL-3.0-or-later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    use_website_for_portal_urls = fields.Boolean(
        string="Use Website URL for Portal Links",
        default=False,
        help="If checked, portal links in emails will use the company's website URL "
        "instead of the standard web.base.url parameter.",
    )