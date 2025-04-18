# © 2025 Numigi
# License LGPL-3.0-or-later (http://www.gnu.org/licenses/lgpl).

import re
from odoo import api, models, tools
from odoo.tools import config, ustr


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _notify_prepare_template_context(self, message, msg_vals=None, **kwargs):
        """Override to replace the base_url in the context with the company's website URL."""
        context = super()._notify_prepare_template_context(message, msg_vals, **kwargs)
        
        # Only modify URLs for records that may have a company
        if hasattr(self, 'company_id'):
            company = self.company_id
            if company and company.use_website_for_portal_urls:
                # Replace the base_url in the context
                base_url = self.env['website'].get_company_website_url(company)
                context['base_url'] = base_url
                
                # Also update any links that were already generated with the old base_url
                old_base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
                if old_base_url != base_url and 'record_url' in context:
                    context['record_url'] = context['record_url'].replace(old_base_url, base_url)
                
        return context
        
    @tools.ormcache('self.company_id.id')
    def _replace_local_links(self, html, base_url=None):
        """Override to use the company's website URL for local links if needed.
        
        This is necessary because some templates might build URLs directly with web.base.url
        before we have a chance to modify the context.
        Uses caching to avoid repeated URL computations.
        """
        if hasattr(self, 'company_id') and self.company_id.use_website_for_portal_urls:
            base_url = self.env['website'].with_context(
                bypass_cache=True).get_company_website_url(self.company_id)
        
        return super()._replace_local_links(html, base_url)

    @api.model
    def _notify_prepare_email_values(self, message, msg_vals=None, **kwargs):
        """Override to replace portal URLs in email body."""
        email_values = super()._notify_prepare_email_values(message, msg_vals, **kwargs)
        
        # Check if we need to replace URLs in the email body
        if hasattr(self, 'company_id') and self.company_id.use_website_for_portal_urls:
            company = self.company_id
            old_base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
            new_base_url = self.env['website'].get_company_website_url(company)
            
            if old_base_url != new_base_url and 'body_html' in email_values:
                html = email_values['body_html']
                if html:
                    # Replace any occurrence of the old URL with the new one
                    email_values['body_html'] = html.replace(old_base_url, new_base_url)
        
        return email_values
