from odoo import models, fields

class ResUsers(models.Model):
    _inherit = "res.partner"

    property_ids = fields.One2many('estate.property', inverse_name="sales_man_id", string='Properties')

