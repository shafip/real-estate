from odoo import models, fields, api, _
from datetime import timedelta
from odoo.exceptions import ValidationError


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Information related to book.'

    title = fields.Char('Title', required=True)
    short_title = fields.Char('Short Title')
    release_date = fields.Date('Release Date')
    internal_notes = fields.Text('Internal Notes')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('lost', 'Lost')],
        'State', default="draft")
    out_of_print = fields.Boolean('Out Of Print', default=False, help='Check stock.')
    number_of_pages = fields.Integer('Number of pages', readonly=False)
    reader_rating = fields.Selection(
        [('week', 'Week'), ('average', 'Average'), ('good', 'Good'), ('excellent', 'Excellent')], string='Reade Rate')
    retail_price = fields.Float('Retail Price', required=True)
    publisher_id = fields.Many2one('library.book.publisher', string='Publisher')
    email = fields.Char(related='publisher_id.email', string='Email')
    phone_number = fields.Char(related='publisher_id.phone_number', string='Phone Number')
    author_ids = fields.Many2many('res.partner', string='Author')
    color = fields.Integer()
    librarian_id = fields.Many2one('res.users', string='Librarian')
    age_days = fields.Integer(string='Age Days', compute='_compute_age_days', inverse='_inverse_age_days', store=True)
    name = fields.Char(compute='_compute_fields_combination')
    category_ids = fields.Many2one('library.book.category', string='Book Category')
    author_names = fields.Char(string='Author Name')

    _sql_constraints = [
        ('title_unique', 'UNIQUE(title)', 'Name already exists'),
        ('number_of_pages_positive', 'CHECK (number_of_pages >= 0)', 'Number of pages must be positive'),
    ]

    @api.onchange('release_date')
    def _onchange_price(self):
        if self.release_date:
            if self.release_date > fields.Date.today():
                raise ValidationError('Release Does Not Make Future ')

    @api.depends('release_date')
    def _compute_age_days(self):
        self.age_days = (fields.Date.today() - self.release_date).days

    def _inverse_age_days(self):
        for record in self:
            if record.age_days:
                record.release_date = (record.release_date - timedelta(days=record.age_days))

    def create_book_category(self):
        category = self.env['library.book.category'].create({
            'name': 'New Category',
            'parent_category_id': '',
            'child_category_ids': self.ids
        })

    def make_available(self):
        print('make_available')
        if self.state == 'draft' or self.state == 'lost' or self.state == 'borrowed':
            self.state = 'available'
        else:
            raise ValidationError('Not Allowed')

    def make_borrowed(self):
        if self.state == 'available':
            self.state = 'borrowed'
        else:
            raise ValidationError('Not Allowed')

    def make_lost(self):
        if self.state == 'borrowed':
            self.state = 'lost'
        else:
            raise ValidationError('Not Allowed')

    @api.depends('title', 'release_date')
    def _compute_fields_combination(self):
        for test in self:
            test.name = test.title + ' ' + str(test.release_date)

    # def _search_age(self, operator, value):
    #     print(value)
    #     if operator not in ['=', '!=']:
    #         raise ValueError(_('This operator is not supported'))
    #     if (operator == '=' and value) or (operator == '!='):
    #         domain = [('age_days', '=', value), ('age_days', '=', value)]
    #         ids = self.env['library.book']._search(domain)
    #     return [('id', 'in', ids)]

    @api.depends('author_ids')
    def get_author_name(self):
        # self.author_names = ", ".join(self.author_ids.mapped('name'))
        self.author_names = ", ".join([rec.name for rec in self.author_ids])

