# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta


class member(models.Model):
    # Socios de la biblioteca
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
        #Existe la secuencia para los carnets?
        sequence = self.env['ir.sequence'].search([('code', '=', 'library.member')])
        #En caso contrario, la creamos
        if not sequence:
            prefix = 'LIB_'
            padding = 4
            implementation = 'no_gap'
            active = True
            sequence = self.env['ir.sequence'].create(
                {'prefix': prefix, 'padding': padding, 'implementation': implementation, 'active': active, 'name': 'Library member Id ', 'code': 'library.member'})
        #Escribimos el valor de la secuencia en el campo correspondiente
        data['membership_number'] = sequence.next_by_id()
        #Devolvemos el nuevo valor
        return super(member, self).create(data)

class book(models.Model):
    # Libros de la biblioteca
    _name = 'library.book'

    name = fields.Char(size=32, string='Book\'s name', index=True)
    id_number = fields.Char(size=32, string='ISBN', index=True)
    date_purchase = fields.Date(string='Date of purchase', default=fields.Datetime.now)
    date_publishing = fields.Date(string='Publishing date')
    active = fields.Boolean('Active', default=True)
    author_id = fields.Many2one('library.author',string='Author')
    publishing_house_id = fields.Many2one('library.publishing_house',string='Publishing House')
    state = fields.Selection([('available', 'Available'), ('lent', 'Lent'), ('out_order', 'Out of order')], string='State', default='available')
    description = fields.Text(string = 'Description')

    _sql_constraints = [('ISBN_uniq', 'unique (id_number)', "ISBN already exists !")]

class author(models.Model):
    # Autores
    _name = 'library.author'

    name = fields.Char(size=32, string='Author\'s name', index=True)
    description = fields.Text(string='Biography')
    book_ids = fields.One2many('library.book','author_id',string='Books in the library')

class publishing_house(models.Model):
    #Editoriales
    _name = 'library.publishing_house'

    name = fields.Char(size=32, string='Publishing house\'s name', index=True)
    description = fields.Text(string='Biography')
    book_ids = fields.One2many('library.book','publishing_house_id',string='Books in the library')

class loan(models.Model):
    #Préstamos
    _name = 'library.loan'

    member_id = fields.Many2one('library.member', string='Member')
    book_id = fields.Many2one('library.book', string='Book', domain="[('state','=','available')]")
    date_loan = fields.Date(string='Date loan', default=fields.Datetime.now)
    date_return = fields.Date(compute='_return_date')
    state = fields.Selection([('new', 'New'), ('1_renewal', 'First renewal'), ('2_renewal', 'Second renewal'), ('out_of_date','Out of date')], string='State', default='new')

    @api.multi
    def _return_date(self):
        for record in self:
            fecha=record.date_loan
            fecha_fin=datetime.strptime(fecha,'%Y-%m-%d')
            record.date_return = fecha_fin + timedelta(days=30)

    @api.model
    def create(self, data):
        libro = self.env['library.book'].search([('id', '=', data['book_id'])])
        libro.state = 'lent'
        return super(loan, self).create(data)


    @api.multi
    def write(self, vals):
        if vals['book_id']:
            libro_antiguo = self.env['library.book'].search([('id', '=', self.book_id.id)])
            libro_antiguo.state='available'
            libro_nuevo = self.env['library.book'].search([('id', '=', vals['book_id'])])
            libro_nuevo.state='lent'
        return super(loan, self).write(vals)

    @api.multi
    def unlink(self):
        libro = self.env['library.book'].search([('id', '=', self.book_id.id)])
        libro.state = 'available'
        return super(loan, self).unlink()

