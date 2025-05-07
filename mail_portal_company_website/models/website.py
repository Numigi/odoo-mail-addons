# Copyright 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import re
from odoo import api, models, tools


class Website(models.Model):
    _inherit = "website"

    @api.model
    def get_company_website_url(self, company=None):
        """Get the website URL for the given company.

        If no company is provided, use the current user's company.
        If company has no website, fall back to default base URL.
        """
        company = company or self.env.company
        default_base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")

        if not company.use_website_for_portal_urls:
            return default_base_url

        website = self.search([("company_id", "=", company.id)], limit=1)

        if not website and company.website:
            cleaned_url = self._sanitize_url(company.website)
            return cleaned_url or default_base_url

        if website:
            domain = website.domain or ""
            if not domain:
                return website.get_base_url()
            cleaned_url = self._sanitize_url(domain)
            return cleaned_url or default_base_url

        return default_base_url

    def _sanitize_url(self, url):
        """Sanitize and normalize a URL string, ensuring http/https and removing unsafe characters."""
        url = (url or '').strip()
        if not url:
            return None

        protocol = 'https://' if url.startswith('https://') else 'http://'

        # Remove existing protocol
        url = re.sub(r'^https?:\/\/', '', url)

        # Remove HTML and unsafe characters
        url = re.sub(r'<[^>]*>', '', url)              # Strip HTML tags
        url = re.sub(r'[^\w\-\.:\/]', '', url)         # Remove unsafe chars

        return protocol + url.rstrip('/')
