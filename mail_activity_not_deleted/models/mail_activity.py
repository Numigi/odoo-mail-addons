# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class MailActivityInactivatedInsteadOfDeleted(models.Model):

    _inherit = 'mail.activity'

    active = fields.Boolean(default=True)

    def action_feedback(self, feedback=False):
        self = self.with_context(mail_activity_no_delete=True)
        return super(MailActivityInactivatedInsteadOfDeleted, self).action_feedback(False)

    @api.multi
    def unlink(self):
        """Deactivate instead of deleting the activity when it is completed."""
        if self._context.get('mail_activity_no_delete'):
            self._send_signal_done()
            self.write({'active': False})
        else:
            return super().unlink()

    def _send_signal_done(self):
        """Send the signal to the chatter that the activity has been completed.

        The code in this method was extracted odoo/addons/mail/models/mail_activity.py.
        """
        for activity in self:
            if activity.date_deadline <= fields.Date.today():
                self.env['bus.bus'].sendone(
                    (self._cr.dbname, 'res.partner', activity.user_id.partner_id.id),
                    {'type': 'activity_updated', 'activity_deleted': True})


class MailActivityMixinWithActivityNotDeletedWhenRecordDeactivated(models.AbstractModel):
    """When deactivating a record, deactivate activities instead of deleting them."""

    _inherit = 'mail.activity.mixin'

    @api.multi
    def write(self, vals):
        if 'active' in vals and vals['active'] is False:
            self = self.with_context(mail_activity_no_delete=True)
        return super(MailActivityMixinWithActivityNotDeletedWhenRecordDeactivated, self).write(vals)
