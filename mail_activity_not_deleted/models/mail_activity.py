# Copyright 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime
from odoo import api, fields, models


class MailActivityInactivatedInsteadOfDeleted(models.Model):
    _inherit = "mail.activity"

    active = fields.Boolean(default=True)
    date_done = fields.Datetime()

    def action_feedback(self, feedback=False, attachment_ids=None):
        self = self.with_context(mail_activity_no_delete=True)
        return super().action_feedback(feedback=feedback, attachment_ids=attachment_ids)

    def unlink(self):
        """Deactivate instead of deleting the activity when it is completed."""
        if self._context.get("mail_activity_no_delete"):
            self._send_signal_done()
            self.write(
                {
                    "active": False,
                    "date_done": datetime.now(),
                }
            )
        else:
            return super().unlink()

    def _send_signal_done(self):
        """Send the signal to the chatter that the activity has been completed."""
        todo_activities = self.filtered(
            lambda act: act.date_deadline <= fields.Date.today()
        )
        if todo_activities:
            # Odoo 18 : On boucle sur chaque partenaire et on utilise _sendone
            for partner in todo_activities.user_id.partner_id:
                self.env["bus.bus"]._sendone(
                    partner, "mail.activity/updated", {"activity_deleted": True}
                )


class MailActivityWithStateDone(models.Model):
    """Add the state done to mail activities."""

    _inherit = "mail.activity"

    state = fields.Selection(selection_add=[("done", "Done")])

    @api.depends("date_deadline", "date_done")
    def _compute_state(self):
        super()._compute_state()
        done_activities = self.filtered(lambda a: a.date_done)
        for activity in done_activities:
            activity.state = "done"
