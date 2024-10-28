# -*- coding: utf-8 -*-
import time
from odoo import api, fields, models, SUPERUSER_ID, _


class fleet_jaujeage(models.Model):
    _name = 'fleet.jaujeage'
    _description = 'Certificat Jaugeage'

    name = fields.Char("Nom")
    creu = fields.Char("Valeur Creux")

class pieces_admin(models.Model):
    _name = 'pieces.admin'
    _description = 'Pieces administratives'

    name = fields.Char("Nom de la pièce", required=1)
    type = fields.Selection([
        ('driver', 'Chaufeur'),
        ('car', 'Vehicule')], string="Concerne", required=1)

class pieces_line(models.Model):
    _name = 'pieces.lines'
    _description = 'Les lignes de Pieces administratives'


    piece_id = fields.Many2one('pieces.admin', "Nom de la piece")
    date_start = fields.Date("Date d'emission")
    date_expi = fields.Date("Date d'expiration")
    fleet_id = fields.Many2one("fleet.vehicle")
    type = fields.Selection([
        ('depot', 'Depot'),
        ('original', 'Original')], string="Concerne")


class fleet(models.Model):
    _inherit = 'fleet.vehicle'

    piece_ids = fields.One2many('pieces.lines', 'fleet_id', "Pièces Administratives",
                                domain="[('type', '=', 'driver')]" )
    partner_id = fields.Many2one('res.partner', string="Noms et Prénoms")
    tel = fields.Char("Numéro de Téléphone")
    subscribteur = fields.Char(string="Souscripteur")
    insurance = fields.Many2one('res.partner', string="Assureur")

    jaugeage_ids = fields.Many2many('fleet.jaujeage', string="Les Compartiments du Certificat Jaujeage")
    driverid = fields.Many2one('fleet.driver', string="Chauffeur")
    company_id = fields.Many2one('res.company', string='Sociéte')

    def name_get(self):
        result = super(fleet, self).name_get()  # Call the parent name_get method
        custom_result = []

        for vehicle_id, name in result:
            # Modify the display name, for example by using only the license plate
            vehicle = self.browse(vehicle_id)
            name = vehicle.license_plate or name  # Use license_plate if it exists, otherwise fallback to the original name
            custom_result.append((vehicle_id, name))

        return custom_result


class fleet_driver(models.Model):
    _name = 'fleet.driver'
    _description = 'Chaufeurs'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner', required=1)
    tel = fields.Char("Numéro de Téléphone")
    company_id = fields.Many2one('res.company', string='Sociéte')
    piece_ids = fields.One2many('pieces.lines', 'fleet_id', "Pièces administrative",
                                domain="[('type', '=', 'driver')]")
    help_driver = fields.Boolean("Est aide Chaufeur ?")


class sms_receiver(models.Model):
    _name = 'sms.recevier'
    _description = 'Recepteur de SMS'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner')
    tel = fields.Char("Numéro de Téléphone")



