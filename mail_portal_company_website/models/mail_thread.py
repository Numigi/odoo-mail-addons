# Copyright 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import re
from odoo import api, models, tools
from odoo.tools import config, ustr


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _notify_prepare_template_context(self, message, msg_vals=None, **kwargs):
        """Override to replace the base_url in the context with the company's website URL."""
        context = super()._notify_prepare_template_context(message, msg_vals, **kwargs)

        # Ensure context has a base_url value by default
        if 'base_url' not in context:
            context['base_url'] = self.env["ir.config_parameter"].sudo().get_param(
                "web.base.url")

        # Only modify URLs for records that may have a company
        if hasattr(self, 'company_id') and self.company_id:
            company = self.company_id
            if company and company.use_website_for_portal_urls:
                # Replace the base_url in the context
                base_url = self.env['website'].get_company_website_url(company)
                context['base_url'] = base_url

                # Also update any links that were already generated with the old base_url
                old_base_url = self.env["ir.config_parameter"].sudo().get_param(
                    "web.base.url")
                if old_base_url != base_url and 'record_url' in context:
                    context['record_url'] = context['record_url'].replace(old_base_url,
                        base_url)

        return context

    def get_base_url(self):
        """Override to return the company website URL when configured.

        By default, return the standard base URL, but if the record has a company
        and the company is configured to use its website URL for portal links,
        return that URL instead.

        Returns:
            str: The base URL to use for this record
        """
        self.ensure_one()

        if hasattr(self, 'company_id') and self.company_id.use_website_for_portal_urls:
            return self.env['website'].get_company_website_url(self.company_id)

        return super().get_base_url()
