# -*- coding: utf-8 -*-
import time
from odoo import api, fields, models, SUPERUSER_ID, _



class driver_follow(models.Model):
    _name = 'driver.suivi'
    _description = 'Suivi  des Chaufeurs'
    _rec_name = 'driver_id'

    driver_id = fields.Many2one('fleet.driver', 'Chauffeur', require=1)
    date = fields.Date("Date de debut")
    date_end = fields.Date("Date de Fin")
    company_id = fields.Many2one('res.company', related='driver_id.company_id', string="Transporteur")

    training_ids = fields.One2many('driver.training', 'suivi_id', "Les Formations")
    bonif_ids = fields.One2many('driver.bonif', 'suivi_id', "Les Bonifications")
    sancion_ids = fields.One2many('driver.sanction', 'suivi_id', "Les Censions")
    incident_ids = fields.One2many('driver.incident','suivi_id',"Les Incidents")
    commnent = fields.Char("Commentaires")






class voyage_incident(models.Model):
    _name = 'driver.incident'
    _description = 'Incident des Chaufeurs'
    _rec_name = 'name'

    def _get_next_reference(self):
        query = """SELECT COUNT(id) AS ligne FROM voyage_incident"""
        self.env.cr.execute(query)
        data = self.env.cr.fetchone()[0]
        year = time.strftime('%Y')
        sort_year = ''

        # on recupère les 2 derniers chiffres
        y = 0
        for i in year:
            y += 1
            if y < 3:
                continue
            sort_year = sort_year + str(i)

        if not data or data == 0:
            return '00001/' + sort_year

        if data < 10:
            return '0000' + str(data + 1) + '/' + sort_year

        if data < 100 and data >= 10:
            return '000' + str(data + 1) + '/' + sort_year

        if data < 1000 and data >= 100:
            return '00' + str(data + 1) + '/' + sort_year

        if data < 10000 and data >= 1000:
            return '0' + str(data + 1) + '/' + sort_year

    name = fields.Char("No Incident", readonly=1, default=lambda self: self._get_next_reference())

    fleet = fields.Many2one("fleet.vehicle", "Remorque Impliqué")
    fleet_t = fields.Many2one("fleet.vehicle", "Tracteur Impliqué")
    date = fields.Date("Date de l'incident")
    voyage = fields.Many2one('livre.voyage')
    place = fields.Char("Lieu de l'incident")
    details = fields.Text("Details de incidents")
    #driver_id = fields.Many2one("fleet.driver", readonly=1)
    suivi_id = fields.Many2one("driver.suivi", readonly=1)
    user_id = fields.Many2one('res.users', 'Enregistrer par :', default=lambda self: self.env.user)

class driver_training(models.Model):
    _name = 'driver.training'
    _description = 'Formations des Chaufeurs'
    _rec_name = 'name'

    partner_id = fields.Many2one('res.partner', string="Formateur")
    name = fields.Char("Initulé Formation")
    date = fields.Date("Date Formation")
    suivi_id = fields.Many2one("driver.suivi", readonly=1)
    user_id = fields.Many2one('res.users', 'Enregistrer par :', default=lambda self: self.env.user)


class driver_bonif(models.Model):
    _name = 'driver.bonif'
    _description = 'Bonifications des Chaufeurs'
    _rec_name = 'name'

    name = fields.Char("Initulé")
    date = fields.Date("Date")
    amount = fields.Integer("Montant")
    suivi_id = fields.Many2one("driver.suivi", readonly=1)
    commnent = fields.Char("Commentaire")
    user_id = fields.Many2one('res.users', 'Enregistrer par :', readonly=1,default=lambda self: self.env.user)


class driver_sanction(models.Model):
    _name = 'driver.sanction'
    _description = 'Santions des Chaufeurs'
    _rec_name = 'name'

    name = fields.Char("Motif")
    date = fields.Date("Date")
    amount = fields.Integer("Montant")
    commnent = fields.Char("Commentaire")
    suivi_id = fields.Many2one("driver.suivi", readonly=1)
    user_id = fields.Many2one('res.users', 'Enregistrer par :',readonly=1, default=lambda self: self.env.user)


