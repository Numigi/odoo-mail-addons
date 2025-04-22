# © 2025 Numigi
# License LGPL-3.0-or-later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestWebsiteURL(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # Create test companies
        cls.company_1 = cls.env["res.company"].create({
            "name": "Test Company 1",
            "website": "https://company1.example.com",
            "use_website_for_portal_urls": True,
        })
        
        cls.company_2 = cls.env["res.company"].create({
            "name": "Test Company 2",
            "website": "company2.example.com",  # No https://
            "use_website_for_portal_urls": True,
        })
        
        cls.company_3 = cls.env["res.company"].create({
            "name": "Test Company 3",
            "website": "https://company3.example.com",
            "use_website_for_portal_urls": False,  # Option disabled
        })
        
        cls.company_4 = cls.env["res.company"].create({
            "name": "Test Company 4",
            # No website defined
            "use_website_for_portal_urls": True,
        })
        
        # Create test websites
        cls.website_1 = cls.env["website"].create({
            "name": "Website 1",
            "domain": "website1.example.com",
            "company_id": cls.company_1.id,
        })
        
        # Note: Company 2 has no website record, only website field
        # Note: Company 3 has option disabled
        # Note: Company 4 has no website at all
        
        # Set base URL param
        cls.env["ir.config_parameter"].sudo().set_param(
            "web.base.url", "https://odoo.example.com"
        )
    
    def test_01_get_company_website_url_with_website_record(self):
        """Test getting URL when company has a website record."""
        url = self.env["website"].get_company_website_url(self.company_1)
        # It should use the website record's URL, not the company.website field
        self.assertTrue("website1.example.com" in url)
    
    def test_02_get_company_website_url_with_website_field_only(self):
        """Test getting URL when company has only website field."""
        url = self.env["website"].get_company_website_url(self.company_2)
        self.assertEqual(url, "http://company2.example.com")
    
    def test_03_get_company_website_url_option_disabled(self):
        """Test getting URL when option is disabled."""
        url = self.env["website"].get_company_website_url(self.company_3)
        self.assertEqual(url, "https://odoo.example.com")
    
    def test_04_get_company_website_url_no_website(self):
        """Test getting URL when no website is defined."""
        url = self.env["website"].get_company_website_url(self.company_4)
        self.assertEqual(url, "https://odoo.example.com")
    
    def test_05_get_company_website_url_invalid_chars(self):
        """Test URL sanitization with invalid characters."""
        test_company = self.env["res.company"].create({
            "name": "Test Company 5",
            "website": "https://invalid<script>alert(1)</script>.example.com",
            "use_website_for_portal_urls": True,
        })
        url = self.env["website"].get_company_website_url(test_company)
        self.assertEqual(url, "https://invalidalert1.example.com")
    
    def test_06_get_company_website_url_trailing_slash(self):
        """Test URL trailing slash handling."""
        test_company = self.env["res.company"].create({
            "name": "Test Company 6",
            "website": "https://test.example.com/path/",
            "use_website_for_portal_urls": True,
        })
        url = self.env["website"].get_company_website_url(test_company)
        self.assertEqual(url, "https://test.example.com/path")
