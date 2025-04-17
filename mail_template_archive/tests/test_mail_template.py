# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import SavepointCase


class TestMailTemplate(SavepointCase):
    """Test the mail template archiving functionality."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.template = cls.env['mail.template'].create({
            'name': 'Test Template',
            'model_id': cls.env.ref('base.model_res_partner').id,
            'subject': 'Test Subject',
            'body_html': '<p>Test Body</p>',
            'email_from': '${object.email|safe}',
            'email_to': '${object.email|safe}',
        })

    def test_archive_single_template(self):
        """Test archiving a single template."""
        self.assertTrue(self.template.active, "Template should be active by default")
        self.template.action_archive()
        self.assertFalse(self.template.active, "Template should be archived")

    def test_unarchive_single_template(self):
        """Test unarchiving a single template."""
        self.template.write({'active': False})
        self.assertFalse(self.template.active, "Template should be inactive")
        self.template.action_unarchive()
        self.assertTrue(self.template.active, "Template should be unarchived")

    def test_archive_multiple_templates(self):
        """Test archiving multiple templates using the group action."""
        template2 = self.template.copy({'name': 'Test Template 2'})
        templates = self.template | template2
        
        for template in templates:
            self.assertTrue(template.active, "Templates should be active by default")
        
        templates.action_archive()
        
        for template in templates:
            self.assertFalse(template.active, "All templates should be archived")

    def test_unarchive_multiple_templates(self):
        """Test unarchiving multiple templates using the group action."""
        template2 = self.template.copy({'name': 'Test Template 2'})
        templates = self.template | template2
        
        templates.write({'active': False})
        for template in templates:
            self.assertFalse(template.active, "Templates should be inactive")
        
        templates.action_unarchive()
        
        for template in templates:
            self.assertTrue(template.active, "All templates should be unarchived")