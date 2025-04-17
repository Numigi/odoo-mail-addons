# mail_template_archive/__manifest__.py
# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Mail Template Archive',
    'version': '12.0.1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Mail',
    'summary': 'Adds the ability to archive email templates',
    'depends': ['mail'],
    'data': [
        'views/mail_template_views.xml',
    ],
    'installable': True,
    'application': False,
}
