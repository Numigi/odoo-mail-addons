# © 2025 Numigi
# License LGPL-3.0-or-later (http://www.gnu.org/licenses/lgpl).

from unittest.mock import patch
from odoo.tests import common
from odoo.addons.mail.models.mail_render_mixin import MailRenderMixin


class TestMailPortal(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # Create test company with website
        cls.company = cls.env["res.company"].create({
            "name": "Test Company",
            "website": "https://test-company.example.com",
            "use_website_for_portal_urls": True,
        })
        
        # Create test website
        cls.website = cls.env["website"].create({
            "name": "Test Website",
            "domain": "test-website.example.com",
            "company_id": cls.company.id,
        })
        
        # Create test partner
        cls.partner = cls.env["res.partner"].create({
            "name": "Test Partner",
            "company_id": cls.company.id,
        })
        
        # Use partner as our test model (it inherits mail.thread)
        cls.test_record = cls.partner
        
        # Set base URL param
        cls.base_url = "https://odoo.example.com"
        cls.env["ir.config_parameter"].sudo().set_param(
            "web.base.url", cls.base_url
        )
    
    def test_01_notify_prepare_template_context(self):
        """Test that the base_url in the context is correctly replaced."""
        
        # Prepare a message
        message = self.env["mail.message"].create({
            "model": "res.partner",
            "res_id": self.test_record.id,
            "body": "Test message",
        })
        
        # Call the method directly to test the override
        context = self.test_record._notify_prepare_template_context(message)
        
        # Check that the base_url is replaced
        self.assertNotEqual(context.get("base_url"), self.base_url)
        self.assertTrue("test-website.example.com" in context.get("base_url"))
    
    def test_02_company_option_disabled(self):
        """Test that the base_url is not replaced when option is disabled."""
        
        # Disable option on company
        self.company.use_website_for_portal_urls = False
        
        # Prepare a message
        message = self.env["mail.message"].create({
            "model": "res.partner",
            "res_id": self.test_record.id,
            "body": "Test message",
        })
        
        # Call the method directly to test the override
        context = self.test_record._notify_prepare_template_context(message)
        
        # Check that the base_url is not replaced
        self.assertEqual(context.get("base_url"), self.base_url)
    
    def test_03_replace_local_links(self):
        """Test that local links are correctly processed."""
        
        # Enable option on company
        self.company.use_website_for_portal_urls = True
        
        # HTML with links using base URL
        html = f"""
        <p>Link to portal: <a href="{self.base_url}/my/partners/123">View Partner</a></p>
        <p>Link to website: <a href="{self.base_url}/shop">Shop</a></p>
        """
        
        # Get company website URL
        company_website_url = self.env["website"].get_company_website_url(self.company)
        
        # Check we have a valid URL
        self.assertTrue(company_website_url)
        self.assertTrue("test-website.example.com" in company_website_url)
        
        # Test the actual link replacement
        result_html = self.test_record._replace_local_links(html)
        
        # Check that base URL was replaced
        self.assertNotIn(self.base_url, result_html)
        self.assertIn(company_website_url, result_html)
    
    def test_04_template_context_urls(self):
        """Test that URLs in template context are replaced correctly."""
        
        # Enable option on company
        self.company.use_website_for_portal_urls = True
        
        # Prepare a message with links using base URL
        body_html = f"""
        <p>Link to portal: <a href="{self.base_url}/my/partners/123">View Partner</a></p>
        <p>Link to website: <a href="{self.base_url}/shop">Shop</a></p>
        """
        
        message = self.env["mail.message"].create({
            "model": "res.partner",
            "res_id": self.test_record.id,
            "body": body_html,
        })
        
        # Call the method directly to test the override
        context = self.test_record._notify_prepare_template_context(message)
        
        # Check that base_url is correctly set in context
        self.assertIn("base_url", context)
        self.assertNotEqual(context["base_url"], self.base_url)
        self.assertTrue("test-website.example.com" in context["base_url"])