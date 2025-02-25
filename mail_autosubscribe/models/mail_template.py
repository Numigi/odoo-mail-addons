# Copyright 2021 Camptocamp (http://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# Backported to v12 by Numigi (https://bit.ly/numigi-com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MailTemplate(models.Model):
    _inherit = "mail.template"

    use_autosubscribe_followers = fields.Boolean(default=True)

    @api.multi
    def generate_recipients(self, results, res_ids):
        res = super().generate_recipients(results, res_ids)
        autosubscribe_followers = (
            self.use_autosubscribe_followers
            and not self.env.context.get("no_autosubscribe_followers")
        )
        if autosubscribe_followers:
            for res_id in res.keys():
                partners = (
                    self.env["res.partner"].sudo().browse(res[res_id]["partner_ids"])
                )
                ResModel = self.env[self.model]
                followers = ResModel._message_get_autosubscribe_followers(partners)
                follower_ids = [
                    follower.id for follower in followers if follower not in partners
                ]
                res[res_id]["partner_ids"] += follower_ids
        return res
