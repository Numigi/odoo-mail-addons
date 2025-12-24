# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/AGPL).

{
    'name': "Mail Bounce Catchall Multi Domain",
    'summary': """
        Fixes the wrong company context in catchall bounce emails for multi-domain environments.
    """,
    'description': """
        In a multi-company environment with different domains, when an email is sent to a
        non-existing alias (triggering the catchall bounce), Odoo standard uses the
        current environment company (often the main company) to render the bounce template.

        This module patches `message_route` to:
        1. Extract the domain from the 'To' email address.
        2. Find the corresponding company.
        3. Force this company in the QWeb rendering context of `mail.mail_bounce_catchall`.
    """,
    'author': "Numigi",
    'website': "https://www.numigi.com",
    'category': 'Discuss',
    'version': '14.0.1.0.1',
    'license': 'AGPL-3',
    'depends': ['mail'],
    'data': [],
    'installable': True,
}
