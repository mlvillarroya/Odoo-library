# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError


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
    date_penalty = fields.Date(string='Date penalty', default=False)
    penalty_state = fields.Char(compute='_penalty_state')

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

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = '(' + record.membership_number + ') ' + record.name
            result.append((record.id, name))
        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            #members = self.search([('name', 'ilike', name)] + args, limit=limit)
            #if not members:
            #members = self.search([('membership_number', 'ilike', name)] + args, limit=limit)
            members = self.search(['|',('name', 'ilike', name),('membership_number', 'ilike', name)] + args, limit=limit)
        else:
            members = self.search(args, limit=limit)
        return members.name_get()

    @api.multi
    def _penalty_state(self):
        for record in self:
            fecha_hoy = fields.datetime.today()
            if (record.date_penalty):
                fecha_pen = datetime.strptime(record.date_penalty, '%Y-%m-%d')
                if (fecha_hoy > fecha_pen):
                    record.update({'date_penalty' : False, 'penalty_state' : ''})
                else:
                    record.update({'penalty_state' : u'lalala'})

class book(models.Model):
    # Libros de la biblioteca
    _name = 'library.book'

    name = fields.Char(size=32, string='Book\'s name', required=True, index=True)
    id_number = fields.Char(size=32, string='ISBN', index=True)
    internal_code = fields.Char(size=32, string='Code', index=True)
    genre_id = fields.Many2one('library.genre', string='Genre', required=True)
    date_purchase = fields.Date(string='Date of purchase', default=fields.Datetime.now)
    date_publishing = fields.Date(string='Publishing date')
    active = fields.Boolean('Active', default=True)
    author_id = fields.Many2one('library.author',string='Author', required=True)
    publishing_house_id = fields.Many2one('library.publishing_house',string='Publishing House')
    state = fields.Selection([('available', 'Available'), ('lent', 'Lent'), ('out_order', 'Out of order')], string='State', default='available')
    description = fields.Text(string = 'Description')

    _sql_constraints = [('ISBN_uniq', 'unique (id_number)', "ISBN already exists !")]

    @api.model
    def create(self, data):
        prefix = self.env['library.genre'].search([('id', '=', data['genre_id'])])
        #Existe la secuencia para los carnets?
        prefix = prefix.code.upper() + '_'
        sequence = self.env['ir.sequence'].search([('code', '=', 'library.book'), ('prefix', '=', prefix)])
        #En caso contrario, la creamos
        if not sequence:
            padding = 4
            implementation = 'no_gap'
            active = True
            sequence = self.env['ir.sequence'].create(
                {'prefix': prefix, 'padding': padding, 'implementation': implementation, 'active': active, 'name': 'Library book Id genre ' + prefix, 'code': 'library.book'})
        #Escribimos el valor de la secuencia en el campo correspondiente
        data['internal_code'] = sequence.next_by_id()
        #Devolvemos el nuevo valor
        return super(book, self).create(data)

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name='(' + record.internal_code + ') ' + record.name
            result.append((record.id, name))
        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            books = self.search(['|',('name', 'ilike', name),('internal_code', 'ilike', name)] + args, limit=limit)
        else:
            books = self.search(args, limit=limit)
        return books.name_get()

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

    member_id = fields.Many2one('library.member', required=True, string='Member')
    book_id = fields.Many2one('library.book', required=True, string='Book', domain="[('state','=','available')]")
    date_loan = fields.Date(string='Date loan', default=fields.Datetime.now)
    date_return = fields.Date(string='Date return')
    state = fields.Selection([('new', 'New'), ('1_renewal', 'First renewal'), ('2_renewal', 'Second renewal'), ('returned','Returned')], string='State', default='new')

    @api.model
    def create(self, data):
        libro = self.env['library.book'].search([('id', '=', data['book_id'])])
        libro.state = 'lent'
        fecha_hoy=fields.datetime.today()
        data['date_return'] = fecha_hoy+timedelta(days=30)
        prestamos = self.env['library.loan'].search([('member_id', '=', data['member_id']),('state', 'in', ['new','1_renewal','2_renewal'])])
        numero_prestamos=len(prestamos)
        if (numero_prestamos>=3):
            raise UserError(_("The maxim numer of loans per person is 3, please return a book before loaning one more"))
        return super(loan, self).create(data)

    @api.multi
    def write(self, vals):
        if (('member_id' in vals) and (vals['member_id'] != self.member_id.id)):
            raise UserError(_("You can't change the member, cancel the loan instead"))
        if (('book_id' in vals) and (vals['book_id'] != self.book_id.id)):
            raise UserError(_("You can't change the book, cancel the loan instead"))
        return super(loan, self).write(vals)

    @api.multi
    def unlink(self):
        for record in self:
            libro = self.env['library.book'].search([('id', '=', record.book_id.id)])
            libro.state = 'available'
        return super(loan, self).unlink()

    @api.multi
    def renew_loan(self):
        fecha_hoy = fields.datetime.today()
        fecha_dev = datetime.strptime(self.date_return, '%Y-%m-%d')
        if (fecha_hoy < fecha_dev):
            fecha_hoy=fields.datetime.today()
            fecha_nueva=fecha_hoy+timedelta(days=30)
            if (self.state != '2_renewal'):
                if (self.state == 'new'):
                    estado='1_renewal'
                elif (self.state == '1_renewal'):
                    estado='2_renewal'
                self.write({'date_return' : fecha_nueva, 'state' : estado})
            else:
                raise UserError(_("You only can renew a loan twice"))
        else:
            raise UserError(_("Your loan is finished, you can't renew it"))

    @api.multi
    def return_loan(self):
        for record in self:
            res = {}
            if ('date_return' in record):
                record.write({'state': 'returned'})
                libro = self.env['library.book'].search([('id', '=', record.book_id.id)])
                libro.write({'state': 'available'})
                fecha_hoy=fields.datetime.today()
                fecha_dev=datetime.strptime(record.date_return,'%Y-%m-%d')
                if (fecha_hoy>fecha_dev):
                    dias_tarde = fecha_hoy-fecha_dev
                    date_penalty = fecha_hoy + dias_tarde
                    member = self.env['library.member'].search([('id', '=', record['member_id'].id)])
                    member.write({'date_penalty' : date_penalty})

                    #CUADRO DE DIALOGO: SANCIÓN
                    view = self.env.ref('library.message_wizard')
                    view_id = view and view.id or False
                    context = dict(self._context or {})
                    context['message'] = 'Por haber entregado el libro '+ str(dias_tarde.days) + ' días tarde, no se podrá efectuar ningún préstamo hasta pasado el ' + datetime.strftime(date_penalty,'%d/%m/%Y')
                    return {
                        'name': 'Sanción',
                        'type': 'ir.actions.act_window',
                        'view_type': 'form',
                        'view_mode': 'form',
                        'view_id': view_id,
                        'res_model': 'library.message',
                        'views': [(view.id, 'form')],
                        'view_id': view.id,
                        'target': 'new',
                        'context': context,
                    }

class genre(models.Model):
    #Géneros de libro
    _name = 'library.genre'

    name = fields.Char(size=32, string='Book\'s genre', index=True)
    code = fields.Char(size=2, string='Code')
    description = fields.Text(string='Description')