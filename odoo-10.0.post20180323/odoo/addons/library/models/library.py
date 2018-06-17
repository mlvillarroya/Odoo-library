# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta


class member(models.Model):
    # Maquinas objeto del librarymiento"""
    _name = 'library.member'

    name = fields.Char(size=32, string='Member name', index=True)
    id_number = fields.Char(size=32, string='DNI/NIE', index=True)
    membership_number = fields.Char('Membership no')
    date_membership = fields.Date(string='Date membership', default=fields.Datetime.now)
    active = fields.Boolean('Active', default=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Char(size=32, string='Adress')
    city = fields.Char(size=32, string='City')
    postalcode = fields.Char('Postal code')

    _sql_constraints = [('DNI_uniq', 'unique (id_number)', "DNI/NIE already exists !")]