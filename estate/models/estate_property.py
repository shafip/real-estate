from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare


class RealEstate(models.Model):
    _name = "estate.property"
    _description = 'Real Estate Table Creation'
    _order = "id desc"

    name = fields.Char(string="Name", required=True)
    postcode = fields.Integer(string="Postcode", required=False)
    description = fields.Text(string="Description", help="Description of the property")
    date_availability = fields.Date(default=lambda self: (datetime.today() + timedelta(days=90)).date(),
                                    string='Date Availability', copy=False, required=True,)
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", copy=False)
    living_area = fields.Integer(string="Living Area", copy=False)
    facades = fields.Integer(string="Facades", required=True, default=1, help="Number of facades of the property")
    garage = fields.Boolean(string="Garage", copy=False)
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation",
        help="Orientation of the garden (North, South, East, or West)")
    active = fields.Boolean('Active', default=True)
    state = fields.Selection([('new', 'New'), ('offer_received', 'Offer Received'),
                              ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'),
                              ('canceled', 'Cancelled')], 'Status', default='new')
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    sales_man_id = fields.Many2one("res.users", default=lambda self: self.env.user, string="Sales_man")
    buyer_id = fields.Many2one("res.partner", copy=False, string="Buyer")
    tag_ids = fields.Many2many("estate.property.tags", string="Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")
    code = fields.Char(related='property_type_id.code')
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area")
    best_offer = fields.Float(compute="_compute_best_offer", string="Best Offer")
    garden = fields.Boolean(string='Garden', default=False, help='Whether there is garden')
    garden_area = fields.Integer(string="Garden Area")


    @api.ondelete(at_uninstall=False)
    def _delete_prevent_property(self):
        for record in self:
            if record.state not in ("new", "canceled"):
                raise exceptions.UserError("Only New And Cancel Is Deleted")

    def action_do_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise exceptions.UserError("Cannot cancel a property that is already sold.")
            record.state = 'sold'

    def action_do_canceled(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError("Cannot mark a canceled property as sold.")
            record.state = 'canceled'

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped('price'))
            else:
                record.best_offer = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10.0
            self.garden_orientation = 'north'
            print("this work on off")
        else:
            self.garden_area = 0.0
            self.garden_orientation = False
            print("this work on")

    @api.constrains("expected_price")
    def _check_expected_price(self):
        for record in self:
            if record.expected_price < 0:
                raise ValidationError("Expected Price Must Be Positive")

    @api.constrains('date_availability')
    def _check_date_availability(self):
        for record in self:
            if record.date_availability < fields.Date.today():
                raise ValidationError("The end date cannot be set in the past")

    @api.constrains('postcode')
    def _check_postcode_minimum(self):
        for record in self:
            if record.postcode and len(str(record.postcode)) < 4:
                raise ValidationError("Postcode must be at least 4 characters long")

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_prices(self):
        for record in self:
            percentage = record.expected_price * 0.9
            if record.selling_price == 0:
                pass
            else:
                if float_compare(record.selling_price, percentage, precision_digits=2) < 0:
                    raise ValidationError("Selling Price Cannot Be Lower Than 90% of the Expected Price.")
