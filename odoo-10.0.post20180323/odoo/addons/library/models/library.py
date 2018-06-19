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


    #Cuando se crea un nuevo socio se genera su número de carnet con la secuencia ir.sequence
    @api.model
    def create(self, data):


        sequence = self.env['ir.sequence'].search([('code', '=', 'library.member')])
        if not sequence:
            prefix = 'LIB_'
            padding = 4
            implementation = 'no_gap'
            active = True
            sequence = self.env['ir.sequence'].create(
                {'prefix': prefix, 'padding': padding, 'implementation': implementation, 'active': active, 'name': 'Library member Id ', 'code': 'library.member'})
        data['membership_number'] = sequence.next_by_id()

        return super(member, self).create(data)
