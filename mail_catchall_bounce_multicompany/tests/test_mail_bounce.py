# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/AGPL).

from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


class TestMailBounceCompany(TransactionCase):

    def setUp(self):
        super(TestMailBounceCompany, self).setUp()

        # 1. Setup Catchall parameters
        self.env['ir.config_parameter'].sudo().set_param('mail.catchall.domain', 'main-domain.com')
        self.env['ir.config_parameter'].sudo().set_param('mail.catchall.alias', 'catchall')
        self.env['ir.config_parameter'].sudo().set_param('mail.catchall.domain.allowed', 'other-domain.com')

        # 2. Create a Main Company
        self.company_main = self.env['res.company'].create({
            'name': 'Main Company Inc',
            'email': 'info@main-domain.com',
        })

        # 3. Create a Secondary Company (Target)
        self.company_secondary = self.env['res.company'].create({
            'name': 'Secondary Target Corp',
            'email': 'contact@other-domain.com',
        })

        # Ensure we are in the main company context initially
        self.env.company = self.company_main

    @mute_logger('odoo.addons.mail.models.mail_thread', 'odoo.models.unlink')
    def test_bounce_catchall_uses_correct_company(self):
        """
        Test that sending an email to 'catchall@other-domain.com' (which has no specific alias)
        triggers a bounce email containing 'Secondary Target Corp' instead of 'Main Company Inc'.
        """

        # Mocking an incoming email dictionary
        message_dict = {
            'message_id': '<12345@external.com>',
            'subject': 'Test Bounce',
            'email_from': 'customer@external.com',
            'to': 'catchall@other-domain.com',  # Addressed to Secondary Company Domain
            'recipients': 'catchall@other-domain.com',
            'references': '',
            'in_reply_to': '',
            'body': 'This is a test body',
        }

        # We use a dummy EmailMessage object as message_route expects it
        import email.message
        msg = email.message.EmailMessage()
        msg['From'] = 'customer@external.com'
        msg['To'] = 'catchall@other-domain.com'
        msg['Message-Id'] = '<12345@external.com>'

        # Trigger message_route.
        # Since 'catchall@...' is the catchall alias but has no specific model alias,
        # and it's a new thread, it should hit the "direct write to catchall" block and return [].

        # We intercept the creation of the bounce email by checking the mail queue
        Mail = self.env['mail.mail']
        existing_mails = Mail.search([])

        # Call the route (this triggers the patch logic)
        self.env['mail.thread'].message_route(msg, message_dict)

        # Check for new mail created
        new_mails = Mail.search([('id', 'not in', existing_mails.ids)])
        self.assertTrue(new_mails, "A bounce email should have been created")

        bounce_mail = new_mails[0]

        # ASSERTIONS
        # The bounce body should contain the name of the Secondary Company
        self.assertIn(
            self.company_secondary.name,
            bounce_mail.body_html,
            "The bounce email should mention the company matching the domain (Secondary Target Corp)"
        )

        # It should NOT contain the Main Company name (unless they are similar strings)
        self.assertNotIn(
            self.company_main.name,
            bounce_mail.body_html,
            "The bounce email should NOT mention the default/main company"
        )

        # Verify the reply-to is also correct
        self.assertIn(
            self.company_secondary.email,
            bounce_mail.reply_to,
            "The Reply-To should be set to the secondary company email"
        )
