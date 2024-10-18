#-*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _


class pieces_admin(models.Model):
    _name = 'pieces.admin'
    _description = 'Pieces administratives'

    name = fields.Char("Nom de la pièce", required=1)
    type = fields.Selection([
        ('driver', 'Chaufeur'),
        ('car', 'Vehicule')], string="Concerne" ,required=1)

class pieces_line(models.Model):
    _name = 'pieces.lines'
    _description = 'Les lignes de Pieces administratives'

    piece_id = fields.Many2one('pieces.admin',"Nom de la piece")
    date_start= fields.Date("Date d'emision")
    date_expi = fields.Date("Date d'expiration")
    fleet_id = fields.Many2one("fleet.vehicle")



class fleet(models.Model):
    _inherit='fleet.vehicle'

    piece_ids = fields.One2many('pieces.lines','fleet_id',"Pieces administrative")

