# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/AGPL).

{
    'name': 'Fetchmail Outlook by company',
    'version': "14.0.1.0.0",
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'AGPL-3',
    'category': 'Other',
    'summary': 'Add the possibility to use Outlook configuration per company.',
    'depends': ['fetchmail_outlook'],
    "data": [
        "views/ir_mail_server_views.xml",
        "views/res_company_views.xml",
        "views/res_config_settings.xml",
    ],
    'installable': True,
}
