# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, fields, models, _

class LibrarySettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _name = 'library.config.settings'

    default_postalcode = fields.Char(default_model='library.member', string='Default postal code')
    num_max_books = fields.Integer()

    @api.model
    def get_default_company_values(self, fields):
        """
        Method argument "fields" is a list of names
        of all available fields.
        """
        company = self.env.user.company_id
        return {
            'num_max_books': company.num_max_books,
        }

    @api.one
    def set_company_values(self):
        company = self.env.user.company_id
        company.num_max_books = self.num_max_books
