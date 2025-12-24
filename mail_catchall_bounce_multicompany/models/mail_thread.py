# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/AGPL).

# -*- coding: utf-8 -*-
import ast
import logging
import re
from email.message import EmailMessage

from odoo import api, models, tools

_logger = logging.getLogger(__name__)


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.model
    def message_route(
        self, message, message_dict, model=None, thread_id=None, custom_values=None
    ):  # noqa: C901
        """
        OVERRIDE: Numigi Patch for Multi-Company Bounce.
        Injects the correct 'res_company' into the bounce template rendering context
        based on the recipient email domain.
        """
        if not isinstance(message, EmailMessage):
            raise TypeError(
                'message must be an email.message.EmailMessage at this point'
            )

        catchall_alias = self.env['ir.config_parameter'].sudo().get_param(
            "mail.catchall.alias"
        )
        catchall_domain_lowered = self.env["ir.config_parameter"].sudo().get_param(
            "mail.catchall.domain", ""
        ).strip().lower()
        catchall_domains_allowed = self.env["ir.config_parameter"].sudo().get_param(
            "mail.catchall.domain.allowed"
        )
        if catchall_domain_lowered and catchall_domains_allowed:
            catchall_domains_allowed = (
                catchall_domains_allowed.split(',') + [catchall_domain_lowered]
            )

        bounce_alias = self.env['ir.config_parameter'].sudo().get_param(
            "mail.bounce.alias"
        )
        bounce_alias_static = tools.str2bool(
            self.env['ir.config_parameter'].sudo().get_param(
                "mail.bounce.alias.static", "False"
            )
        )
        fallback_model = model

        # get email.message.Message variables for future processing
        message_id = message_dict['message_id']

        # compute references to find if message is a reply to an existing thread
        thread_references = message_dict['references'] or message_dict['in_reply_to']
        msg_references = [
            re.sub(r'[\r\n\t ]+', r'', ref)  # "Unfold" buggy references
            for ref in tools.mail_header_msgid_re.findall(thread_references)
            if 'reply_to' not in ref
        ]
        mail_messages = self.env['mail.message'].sudo().search(
            [('message_id', 'in', msg_references)], limit=1, order='id desc, message_id'
        )
        is_a_reply = bool(mail_messages)
        reply_model, reply_thread_id = mail_messages.model, mail_messages.res_id

        # author and recipients
        email_from = message_dict['email_from']
        email_from_localpart = (
            tools.email_split(email_from) or ['']
        )[0].split('@', 1)[0].lower()
        email_to = message_dict['to']
        email_to_localparts = [
            e.split('@', 1)[0].lower()
            for e in (tools.email_split(email_to) or [''])
        ]
        rcpt_tos_localparts = []
        for recipient in tools.email_split(message_dict['recipients']):
            to_local, to_domain = recipient.split('@', maxsplit=1)
            if (
                not catchall_domains_allowed
                or to_domain.lower() in catchall_domains_allowed
            ):
                rcpt_tos_localparts.append(to_local.lower())
        rcpt_tos_valid_localparts = [to for to in rcpt_tos_localparts]

        # 0. Handle bounce
        if bounce_alias and any(
            email.startswith(bounce_alias) for email in email_to_localparts
        ):
            # Regex raw string fix
            bounce_re = re.compile(
                r"%s\+(\d+)-?([\w.]+)?-?(\d+)?" % re.escape(bounce_alias), re.UNICODE
            )
            bounce_match = bounce_re.search(email_to)
            if bounce_match:
                self._routing_handle_bounce(message, message_dict)
                return []
        if (
            bounce_alias
            and bounce_alias_static
            and any(email == bounce_alias for email in email_to_localparts)
        ):
            self._routing_handle_bounce(message, message_dict)
            return []
        if (
            message.get_content_type() == 'multipart/report'
            or email_from_localpart == 'mailer-daemon'
        ):
            self._routing_handle_bounce(message, message_dict)
            return []
        self._routing_reset_bounce(message, message_dict)

        # 1. Handle reply
        if reply_model and reply_thread_id:
            other_model_aliases = self.env['mail.alias'].search([
                '&', '&',
                ('alias_name', '!=', False),
                ('alias_name', 'in', email_to_localparts),
                ('alias_model_id.model', '!=', reply_model),
            ])
            if other_model_aliases:
                is_a_reply = False
                rcpt_tos_valid_localparts = [
                    to for to in rcpt_tos_valid_localparts
                    if to in other_model_aliases.mapped('alias_name')
                ]

        if is_a_reply:
            dest_aliases = self.env['mail.alias'].search([
                ('alias_name', 'in', rcpt_tos_localparts),
                ('alias_model_id.model', '=', reply_model)
            ], limit=1)

            user_id = self._mail_find_user_for_gateway(
                email_from, alias=dest_aliases
            ).id or self._uid
            route = self._routing_check_route(
                message, message_dict,
                (reply_model, reply_thread_id, custom_values, user_id, dest_aliases),
                raise_exception=False)
            if route:
                _logger.info(
                    'Routing mail from %s to %s with Message-Id %s: '
                    'direct reply to msg: model: %s, thread_id: %s, '
                    'custom_values: %s, uid: %s',
                    email_from, email_to, message_id, reply_model,
                    reply_thread_id, custom_values, self._uid)
                return [route]
            elif route is False:
                return []

        # 2. Handle new incoming email
        if rcpt_tos_localparts:
            message_dict.pop('parent_id', None)

            # check it does not directly contact catchall
            if (
                catchall_alias
                and email_to_localparts
                and all(
                    email_localpart == catchall_alias
                    for email_localpart in email_to_localparts
                )
            ):
                _logger.info(
                    'Routing mail from %s to %s with Message-Id %s: '
                    'direct write to catchall, bounce',
                    email_from, email_to, message_id
                )

                # --- START NUMIGI PATCH ---
                # Attempt to find the target company based on the recipient domain
                target_company = self.env.company
                try:
                    email_list = tools.email_split(email_to)
                    if email_list:
                        # Extract domain (e.g., 'avrexcanada.com')
                        domain = email_list[0].split('@')[-1]

                        # Find company matching the domain (by email or name)
                        company_match = self.env['res.company'].search([
                            '|',
                            ('email', 'ilike', domain),
                            ('name', 'ilike', domain)
                        ], limit=1)

                        if company_match:
                            target_company = company_match
                except Exception as e:
                    _logger.warning(
                        "Mail Bounce Fix: Failed to determine company from domain: %s", e
                    )

                # Render with the specific company in context
                body = self.env.ref('mail.mail_bounce_catchall')._render({
                    'message': message,
                    'res_company': target_company,  # Pass the correct company
                }, engine='ir.qweb')

                # Use target company email for reply-to if available
                reply_to_email = (
                    target_company.email or self.env.company.email
                )
                # --- END NUMIGI PATCH ---

                self._routing_create_bounce_email(
                    email_from, body, message,
                    references=message_id, reply_to=reply_to_email
                )
                return []

            dest_aliases = self.env['mail.alias'].search(
                [('alias_name', 'in', rcpt_tos_valid_localparts)]
            )
            if dest_aliases:
                routes = []
                for alias in dest_aliases:
                    user_id = self._mail_find_user_for_gateway(
                        email_from, alias=alias
                    ).id or self._uid
                    route = (
                        alias.alias_model_id.model,
                        alias.alias_force_thread_id,
                        ast.literal_eval(alias.alias_defaults),
                        user_id,
                        alias
                    )
                    route = self._routing_check_route(
                        message, message_dict, route, raise_exception=True
                    )
                    if route:
                        _logger.info(
                            'Routing mail from %s to %s with Message-Id %s: '
                            'direct alias match: %r',
                            email_from, email_to, message_id, route)
                        routes.append(route)
                return routes

        # 3. Fallback
        if fallback_model:
            message_dict.pop('parent_id', None)
            user_id = self._mail_find_user_for_gateway(email_from).id or self._uid
            route = self._routing_check_route(
                message, message_dict,
                (fallback_model, thread_id, custom_values, user_id, None),
                raise_exception=True)
            if route:
                _logger.info(
                    'Routing mail from %s to %s with Message-Id %s: '
                    'fallback to model:%s, thread_id:%s, custom_values:%s, uid:%s',
                    email_from, email_to, message_id, fallback_model,
                    thread_id, custom_values, user_id)
                return [route]

        raise ValueError(
            'No possible route found for incoming message from %s to %s '
            '(Message-Id %s:). '
            'Create an appropriate mail.alias or force the destination model.' %
            (email_from, email_to, message_id)
        )
