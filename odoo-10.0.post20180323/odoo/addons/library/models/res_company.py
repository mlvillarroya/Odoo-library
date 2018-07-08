# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api

class Company(models.Model):
    _inherit = 'res.company'

    num_max_books=fields.Integer(string="Maximum number of books in one loan")