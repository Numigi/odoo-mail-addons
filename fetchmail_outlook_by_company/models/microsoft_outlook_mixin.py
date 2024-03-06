# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/AGPL).

import json
import logging
import requests

from werkzeug.urls import url_encode, url_join

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class MicrosoftOutlookMixin(models.AbstractModel):
    _inherit = "microsoft.outlook.mixin"

    company_id = fields.Many2one(
        'res.company', required=True, default=lambda self: self.env.company)

    def _check_current_company_config(self):
        if self.company_id:
            return (
                self.company_id.microsoft_outlook_client_identifier
                and self.company_id.microsoft_outlook_client_secret
            )
        else:
            return False

    @api.depends("use_microsoft_outlook_service", 'company_id')
    def _compute_is_microsoft_outlook_configured(self):
        if self._check_current_company_config():
            microsoft_outlook_client_id = self.company_id.microsoft_outlook_client_identifier
            microsoft_outlook_client_secret = self.company_id.microsoft_outlook_client_secret
            self.is_microsoft_outlook_configured = (
                microsoft_outlook_client_id and microsoft_outlook_client_secret
            )
        else:
            super()._compute_is_microsoft_outlook_configured()

    def _compute_outlook_uri_by_company(self):
        base_url = self.get_base_url()
        for record in self:
            microsoft_outlook_client_id = record.company_id.microsoft_outlook_client_identifier
            if (
                not record.id
                or not record.use_microsoft_outlook_service
                or not record.company_id
                or not record.is_microsoft_outlook_configured
            ):
                record.microsoft_outlook_uri = False
                continue

            record.microsoft_outlook_uri = url_join(
                self._get_microsoft_endpoint(),
                "authorize?%s"
                % url_encode(
                    {
                        "client_id": microsoft_outlook_client_id,
                        "response_type": "code",
                        "redirect_uri": url_join(
                            base_url, "/microsoft_outlook/confirm"
                        ),
                        "response_mode": "query",
                        # offline_access is needed to have the refresh_token
                        "scope": "offline_access %s" % self._OUTLOOK_SCOPE,
                        "state": json.dumps(
                            {
                                "model": record._name,
                                "id": record.id,
                                "csrf_token": record._get_outlook_csrf_token(),
                            }
                        ),
                    }
                ),
            )

    @api.depends('use_microsoft_outlook_service', 'company_id')
    def _compute_outlook_uri(self):
        if self._check_current_company_config():
            self._compute_outlook_uri_by_company()
        else:
            super()._compute_is_microsoft_outlook_configured()

    def _fetch_outlook_token_by_company(self, grant_type, **values):
        base_url = self.get_base_url()
        microsoft_outlook_client_id = self.company_id.microsoft_outlook_client_identifier
        microsoft_outlook_client_secret = self.company_id.microsoft_outlook_client_secret

        response = requests.post(
            url_join(self._get_microsoft_endpoint(), 'token'),
            data={
                'client_id': microsoft_outlook_client_id,
                'client_secret': microsoft_outlook_client_secret,
                'scope': 'offline_access %s' % self._OUTLOOK_SCOPE,
                'redirect_uri': url_join(base_url, '/microsoft_outlook/confirm'),
                'grant_type': grant_type,
                **values,
            },
            timeout=10,
        )

        if not response.ok:
            try:
                error_description = response.json()['error_description']
            except Exception:
                error_description = _('Unknown error.')
            raise UserError(
                _('An error occurred when fetching the access token. %s') % error_description)

        return response.json()

    def _fetch_outlook_token(self, grant_type, **values):
        if self._check_current_company_config():
            self._fetch_outlook_token_by_company(grant_type, **values)
        else:
            super()._fetch_outlook_token(grant_type, **values)
