# -*- coding: utf-8 -*-
from odoo import  models, fields, api
from datetime import date
from dateutil import relativedelta
import time
from dateutil import parser

class Circuit(models.Model):
    _name = 'karting.circuit'
    name = fields.Char('Circuit', size=15, required=True)

class Racer(models.Model):

    _name = 'karting.racer'

    first_name = fields.Char('First name', size=30, required=True)
    last_name = fields.Char('Last name', size=40, required=True)
    fullName = fields.Char(string='Full Name', compute='comp_name')
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

    @api.depends('first_name', 'last_name')
    def comp_name(self):
        for test in self:
                    test.fullName = test.first_name + ' ' + test.last_name

class Diary(models.Model):

    @api.depends('date')
    def comp_name(self):
        for test in self:
                    test.name =  test.date , ' ' , test.circuit_id.name

    _name = 'karting.diary'
    name = fields.Char(string='Fecha', compute='comp_name')
    date = fields.Date('Date', required=True, default=lambda *a: time.strftime('%Y-%m-%d'))
    circuit_id = fields.Many2one('karting.circuit', 'Circuit', required=True)
    obs = fields.Text ('Observations')
    racer_ids = fields.One2many('karting.diary.racer', 'diary_id', 'Racers')
    rounds_ids = fields.One2many('karting.round', 'diary_id', 'Rounds')
    active = fields.Boolean('Active', default=True)

class DiaryRacer(models.Model):

    def major(self):
        for test in self:
            if str(parser.parse(test.diary_id.date) - relativedelta.relativedelta(years=18)) >= test.racer_id.birthdate:
                return True
            else:
                return False

    def cumple_func(self):
        for test in self:
            for x in test.racer_id:
                return x.birthdate

    _name = 'karting.diary.racer'
    racer_id = fields.Many2one('karting.racer', 'Racer', required=True)
    diary_id = fields.Many2one('karting.diary', 'Diary', required=True)
    major_edad = fields.Boolean(compute='major', string='Edad', default=False)
    cumple = fields.Date(compute='cumple_func', string='Cumple', store=True)
    kart_type_id = fields.Many2one('karting.kart_type', 'Type of kart', required=True)
    group_id = fields.Many2one('karting.racer.group', 'Group')
    tutor = fields.Char('Tutor', size=40)
    tutor_doc = fields.Char('Tutors doc', size=40)
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
    name = fields.Char(compute='comp_name', string='Ronda', store=True)
    tiempo = fields.Float('Inicio')
    diary_id = fields.Many2one('karting.diary', 'Diary')
    racer_ids = fields.One2many('karting.diary.racer', 'round_id', 'Racers', readonly = True)

    @api.depends('diary_id')
    def comp_name(self):
        for test in self:
            prueba = "Circuito: " + test.diary_id.name
            test.name = ("Tiempo: ", "%02d:%02d" % (int(test.tiempo), (test.tiempo - int(test.tiempo)) * 60), prueba)


