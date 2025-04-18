# © 2025 Numigi
# License LGPL-3.0-or-later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class Website(models.Model):
    _inherit = "website"

    @api.model
    def get_company_website_url(self, company=None):
        """Get the website URL for the given company.
        
        If no company is provided, use the current user's company.
        If company has no website, fall back to default base URL.
        
        Returns:
            str: The website URL to use for portal links
        """
        if not company:
            company = self.env.company
            
        if not company.use_website_for_portal_urls:
            return self.env["ir.config_parameter"].sudo().get_param("web.base.url")
            
        # Try to find website tied to the company
        website = self.search([("company_id", "=", company.id)], limit=1)
        if not website and company.website:
            # If no website record is linked but company has website URL field set
            # Clean and return company.website value
            website_url = company.website
            if not website_url.startswith(('http://', 'https://')):
                website_url = 'https://' + website_url
            return website_url
            
        if website:
            return website.get_base_url()
            
        # Fallback to default
        return self.env["ir.config_parameter"].sudo().get_param("web.base.url")