from odoo import models, fields


class LibraryBookPublisher(models.Model):
    _name = "library.book.publisher"
    _description = "Information about the publisher"

    name = fields.Char('Publisher', required='True')
    email = fields.Char('Email')
    phone_number = fields.Char('Phone Number')
    published_books_ids = fields.One2many('library.published.books', 'publisher_id', 'Published Books')
