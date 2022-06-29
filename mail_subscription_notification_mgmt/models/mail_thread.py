# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.multi
    def _message_auto_subscribe_notify(self, partner_ids, template):
        if self and self.env['ir.model']._get(self[0]._name).disable_subscription_notification:
            return
        return super(MailThread, self)._message_auto_subscribe_notify(
            partner_ids, template)
