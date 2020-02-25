#-*- coding: utf-8 -*-
from odoo import models, fields, api

class Categoria(models.Model):
    _name = 'libro.categoria'
    name = fields.Char('Nombre Categoria')

class LibroTask(models.Model):
    _inherit = 'libro.task'
    isbn = fields.Char('Isbn')
    precio = fields.Float('Precio')
    resumen = fields.Text('Resumen')
    fecha = fields.Date('Fecha')
    revisado = fields.Boolean('Revisado')
    aprobado = fields.Selection([('si','si'),('no','no'),('pendiente','pendiente')])
    categoria = fields.Many2one('libro.categoria','categoria')


