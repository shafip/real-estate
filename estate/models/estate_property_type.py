from odoo import models, fields, api


class RealEstate(models.Model):
    _name = "estate.property.type"
    _description = 'Real Estate Property Type'
    _order = "name desc"

    name = fields.Char(string="Name", required=True, size=40)
    code = fields.Char(string="Code", size=20)
    property_type_ids = fields.One2many("estate.property", inverse_name="property_type_id")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many("estate.property.offer", inverse_name="property_type_id")
    offer_count = fields.Char(compute="_compute_offer_count")

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Name already exists'),
        ('code_unique', 'UNIQUE(code)', 'Code already exists'),
    ]

    def _compute_offer_count(self):
        self.offer_count = sum(len(record.offer_ids) for record in self)

    @api.depends("offer_ids")
    def stat_offer_action(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Property Offer",
            "res_model": "estate.property.offer",
            "view_mode": "tree",
            # 'view_id': self.env.ref('estate.estate_property_type_view_tree').id,
            "domain": [("property_type_id", "=", self.name)],
        }
