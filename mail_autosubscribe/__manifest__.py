# Copyright 2021 Camptocamp (http://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# Backported to v12 by Numigi (https://bit.ly/numigi-com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Mail Autosubscribe",
    "summary": "Automatically subscribe partners to its company's business documents",
    "version": "12.0.1.0.0",
    "author": "Camptocamp, Numigi, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Marketing",
    "depends": ["mail"],
    "maintainer": "Numigi",
    "website": "https://github.com/OCA/social",
    "data": [
        "security/ir.model.access.csv",
        "views/mail_autosubscribe_views.xml",
        "views/mail_template.xml",
        "views/res_partner_views.xml",
    ],
}
