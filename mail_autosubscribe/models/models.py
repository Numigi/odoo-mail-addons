# Copyright 2021 Camptocamp (http://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# Backported to v12 by Numigi (https://bit.ly/numigi-com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class BaseModel(models.AbstractModel):
    _inherit = "base"

    @api.model
    def _message_get_autosubscribe_followers_domain(self, partners):
        commercial_partner_ids = partners.mapped("commercial_partner_id").ids
        return [
            ("id", "child_of", commercial_partner_ids),
            ("mail_autosubscribe_ids.model", "=", self._name),
        ]

    @api.model
    def _message_get_autosubscribe_followers(self, partners):
        domain = self._message_get_autosubscribe_followers_domain(partners)
        return self.env["res.partner"].sudo().search(domain)
