# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, fields, models, _

class LibrarySettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _name = 'library.config.settings'

    default_postalcode = fields.Char(default_model='library.member', string='Default postal code')
    default_city = fields.Char(default_model='library.member', string='Default city')
    num_max_books=fields.Integer(string="Maximum number of books in one loan")
    penalize_late_loans=fields.Boolean(string="Penalize loans that return late")
    penalty_days_per_day=fields.Float(string="Penalty days per day late (can be decimal)")
    loan_days=fields.Integer(string="Days a loan lasts")

    @api.model
    def get_default_loan_values(self, fields):
        """
        Method argument "fields" is a list of names
        of all available fields.
        """
        company = self.env.user.company_id
        return {
            'loan_days':company.loan_days,
            'num_max_books': company.num_max_books,
            'penalize_late_loans': company.penalize_late_loans,
            'penalty_days_per_day': company.penalty_days_per_day,

        }

    @api.one
    def set_loan_values(self):
        company = self.env.user.company_id
        company.loan_days = self.loan_days
        company.num_max_books = self.num_max_books
        company.penalize_late_loans = self.penalize_late_loans
        company.penalty_days_per_day = self.penalty_days_per_day
