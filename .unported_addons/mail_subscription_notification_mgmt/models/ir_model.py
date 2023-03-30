# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


class IrModel(models.Model):
    _inherit = 'ir.model'

    disable_subscription_notification = fields.Boolean("Disable Subscription Notifications")
