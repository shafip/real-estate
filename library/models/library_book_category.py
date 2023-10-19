from odoo import models, fields


class LibraryBookCategory(models.Model):
    _name = "library.book.category"


    name = fields.Char('Name', required='True')
    parent_category_id = fields.Many2one('library.book.category')
    child_category_ids = fields.One2many('library.book.category', inverse_name='parent_category_id')

