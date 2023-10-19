from odoo import models, fields


class LibraryPublishedBooks(models.Model):
    _name = 'library.published.books'
    _description = 'Published books details'

    name_id = fields.Many2one('library.book', required=True, string='Name')
    release_date = fields.Date(string='Release date')
    publisher_id = fields.Many2one('library.book.publisher', required=True)
