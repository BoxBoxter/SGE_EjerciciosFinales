# -*- coding: utf-8 -*-
from odoo import  models, fields, api
from datetime import datetime

class Circuit(models.Model):
    _name = 'karting.circuit'
    name = fields.Char('Circuit', size=15, required=True)



class Racer(models.Model):
    _name = 'karting.racer'

    first_name = fields.Char('First name', size=30, required=True)
    last_name = fields.Char('Last name', size=40, required=True)

    fullName = fields.Char(compute='comp_name', store=False, size=100)

    birthdate = fields.Date('BirthDate', required=True)
    phone = fields.Char('Phone', size=20)
    email = fields.Char('eMail', size=60)
    address = fields.Char('Address', size=60)
    zip = fields.Char('Zip', size=5)
    city = fields.Char('City', size=30)
    state_id = fields.Many2one('res.country.state', 'State')
    country_id = fields.Many2one('res.country', 'Country')
    race_ids = fields.One2many('karting.diary.racer', 'racer_id', 'Racers', readonly=True)
    active = fields.Boolean('Active', default=True)

    @api.multi
    @api.depends('first_name', 'last_name')
    def comp_name(self):
        self.fullName = self.first_name
        #(self.first_name)#)+' '+(self.last_name or '')


class Diary(models.Model):
    _name = 'karting.diary'
    date = fields.Date('Date', required=True)
    circuit_id = fields.Many2one('karting.circuit', 'Circuit', required=True)
    #circuit_name = fields.related('circuit_id','name')
    obs = fields.Text ('Observations')
    racer_ids = fields.One2many('karting.diary.racer', 'diary_id', 'Racers')
    rounds_ids = fields.One2many('karting.round', 'diary_id', 'Rounds')
    active = fields.Boolean('Active', default=True)

class DiaryRacer(models.Model):
    _name = 'karting.diary.racer'
    racer_id = fields.Many2one('karting.racer', 'Racer', required=True)
    diary_id = fields.Many2one('karting.diary', 'Diary', required=True)
    kart_type_id = fields.Many2one('karting.kart_type', 'Type of kart', required=True)
    group_id = fields.Many2one('karting.racer.group', 'Group')
    tutor = fields.Char('Tutor', size=40)
    tutor_doc = fields.Char('Tutors doc.', size=40, help='Document (type and number)'),
    round_id = fields.Many2one('karting.round', 'Round')

class KartType(models.Model):
    _name = 'karting.kart_type'
    name = fields.Char('Type', size=30, required=True)
    cilinder_capacity = fields.Integer('Cilinder Capacity (cc)')

class RacerGroup(models.Model):
    _name = 'karting.racer.group'
    name = fields.Char('Group', size=30)
    race_ids = fields.One2many('karting.diary.racer', 'group_id', 'Racers')

class Round(models.Model):
    _name = 'karting.round'
    name = fields.Char('Round', size=30)
    tiempo = fields.Float('Inicio')
    diary_id = fields.Many2one('karting.diary', 'Diary')
    racer_ids = fields.One2many('karting.diary.racer', 'round_id', 'Racers', readonly = True)



