# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime

from odoo import fields
from odoo.tests import common


class TestMailActivity(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env.ref('base.res_partner_2')
        cls.activity = cls.env['mail.activity'].create({
            'res_id': cls.partner.id,
            'res_model_id': cls.env.ref('base.model_res_partner').id,
            'date_deadline': datetime.now(),
            'user_id': cls.env.user.id,
        })

    def test_when_activity_is_completed_then_it_is_inactive_instead_of_deleted(self):
        self.assertTrue(self.activity.active)

        self.activity.action_done()
        self.assertTrue(self.activity.exists())
        self.assertFalse(self.activity.active)

    def test_when_record_is_deactivated_then_the_activity_is_inactive_instead_of_deleted(self):
        self.assertTrue(self.activity.active)

        self.partner.active = False
        self.activity.refresh()
        self.assertTrue(self.activity.exists())
        self.assertFalse(self.activity.active)

    def test_the_date_done_is_computed_when_the_activity_is_completed(self):
        self.assertFalse(self.activity.date_done)

        time_before = datetime.now()
        self.activity.action_done()
        time_after = datetime.now()

        date_done = fields.Datetime.from_string(self.activity.date_done)
        self.assertLessEqual(time_before, date_done)
        self.assertLessEqual(date_done, time_after)
