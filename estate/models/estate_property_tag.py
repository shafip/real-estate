from odoo import models, fields

class EstatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = 'Real Estate Property tags '
    _order = "name desc"

    name = fields.Char(required=True, string="Name", size=40)
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Name already exists'),
    ]
