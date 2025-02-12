# Copyright 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class MailActivityMixinWithActivityNotDeletedWhenRecordDeactivated(
    models.AbstractModel
):
    """When deactivating a record, deactivate activities instead of deleting them."""

    _inherit = "mail.activity.mixin"

    def write(self, vals):
        if "active" in vals and vals["active"] is False:
            self = self.with_context(mail_activity_no_delete=True)
        return super().write(vals)
