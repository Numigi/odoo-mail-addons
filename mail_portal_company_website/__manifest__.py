# © 2025 Numigi
# License LGPL-3.0-or-later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Mail Portal Company Website",
    "version": "14.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://www.numigi.com",
    "license": "LGPL-3",
    "category": "Mail",
    "summary": "Use company website URL for portal links in emails",
    "depends": [
        "mail",
        "portal",
        "website",
    ],
    "data": [
        "views/res_company_views.xml",
    ],
    "installable": True,
}