# Copyright 2021 Camptocamp (http://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# # Backported to v12 by Numigi (https://bit.ly/numigi-com).).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    mail_autosubscribe_ids = fields.Many2many(
        "mail.autosubscribe",
        string="Autosubscribe Models",
        column1="partner_id",
        column2="model_id",
    )
