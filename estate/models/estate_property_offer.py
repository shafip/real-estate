from odoo import models, fields, api, exceptions
from datetime import timedelta
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = 'Estate Property offer'
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[('refused', 'Refused'), ('accepted', 'Accepted'), ('none', 'None')],
        default="none",
        string="Status",
        help="Select corresponding status for this",
        copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="Validity(days)", default=7)
    create_date = fields.Datetime(string="Creation Date", readonly=True, default=lambda self: fields.datetime.now())
    deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline", string="Deadline")
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", store=True)

    @api.model
    def create(self, vals):
        if vals.get('status') == 'accepted':
            self.search([('status', 'in', ('none', 'accepted'))]).write({'status': 'refused'})
        return super(EstatePropertyOffer, self).create(vals)

    def write(self, vals):
        if vals.get('status') == 'accepted':
            self.search([('status', 'in', ('none', 'accepted'))]).write({'status': 'refused'})
        return super(EstatePropertyOffer, self).write(vals)

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            if record.validity:
                record.deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.deadline:
                record.validity = (record.deadline - fields.Date.today()).days
            else:
                record.validity = 0

    def action_accept(self):
        for record in self:
            record.status = "accepted"
            if record.property_id:
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
                record.property_id.state = "offer_accepted"

    def action_refuse(self):
        for record in self:
            record.status = "refused"
            if record.property_id:
                record.property_id.state = "new"
                record.property_id.selling_price = 0
                record.property_id.buyer_id = ''
        return True

    @api.constrains('price')
    def check_positive(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError("A property offer price must be positive")

    @api.model
    def create(self, vals):
        property_id = vals.get('property_id')
        print(property_id)
        price = vals.get('price', 0.0)
        existing_offers = self.env['estate.property.offer'].search([('property_id', '=', property_id)])
        if existing_offers:
            for offer in existing_offers:
                if price < offer.price:
                    raise exceptions.ValidationError(
                        "New offer price cannot be lower than an existing offer price: {}".format(offer.price))
        return super(EstatePropertyOffer, self).create(vals)

    @api.constrains('price')
    def _onchange_price(self):
        for record in self:
            if record.price:
                record.property_id.state = "offer_received"
