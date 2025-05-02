# © 2025 Numigi
# License LGPL-3.0-or-later (http://www.gnu.org/licenses/lgpl).

import re
from odoo import api, models, tools


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
            website_url = (company.website or '').strip()
            if not website_url:
                return self.env["ir.config_parameter"].sudo().get_param("web.base.url")
            
            # Ensure protocol
            website_url = website_url.strip()
            
            # Keep the original protocol if it exists
            if website_url.startswith('https://'):
                protocol = 'https://'
            else:
                protocol = 'http://'
                
            # Remove any existing protocol for processing
            if website_url.startswith(('http://', 'https://')):
                website_url = re.sub(r'^https?:\/\/', '', website_url)
                
            # Remove dangerous characters
            website_url = re.sub(r'<[^>]*>', '', website_url)  # Remove HTML tags
            website_url = re.sub(r'[^\w\-\.:\/]', '', website_url)  # Remove other unsafe chars
            
            # Add protocol back
            return protocol + website_url.rstrip('/')
            
        if website:
            # Construct the URL using the website domain instead of calling get_base_url()
            domain = website.domain or ""
            if not domain:
                return website.get_base_url()
                
            # Ensure protocol
            if domain.startswith('https://'):
                protocol = 'https://'
            else:
                protocol = 'http://'
                
            # Remove any existing protocol for processing
            if domain.startswith(('http://', 'https://')):
                domain = re.sub(r'^https?:\/\/', '', domain)
                
            # Return with protocol
            return protocol + domain.rstrip('/')
            
        # Fallback to default
        return self.env["ir.config_parameter"].sudo().get_param("web.base.url")
