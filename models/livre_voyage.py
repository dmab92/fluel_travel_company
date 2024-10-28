#-*- coding: utf-8 -*-
import time
from odoo import models, fields, api
import urllib, requests
from datetime import datetime as dt

class livre_voyage(models.Model):
    _name = 'livre.voyage'
    _description = "Bon Livre de Voyage"
    _rec_name ='number'


    def _get_next_reference(self):
        query = """SELECT COUNT(id) AS ligne FROM livre_voyage"""
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

#---------BON D'ENLEVEMENT------------------------------#

    number = fields.Char(readonly="True", default=lambda self: self._get_next_reference())

    name = fields.Char("Bon d'enlevement No")
    #date_register = fields.Date("Date d'enregitrement")
    user_id = fields.Many2one('res.users', 'Enregistrer par :', readonly=1, default=lambda self: self.env.user)
    date_bon = fields.Date("Date du bon d'enlevement")
    client = fields.Many2one("res.partner", "Client")
    quantity = fields.Integer("Quantite")
    price_unit = fields.Integer("Pu")
    amount = fields.Integer("Montant Transport Carburant", compute="_amount_price",
                            help="Il s'agit du montant du transort du carbutant, quantite * pu",
                            )
    fleet = fields.Many2one("fleet.vehicle","Immatriculation Remorque")
    fleet_t = fields.Many2one("fleet.vehicle", "Immatriculation Tracteur")
    driver= fields.Many2one('fleet.driver','Chauffeur')
    livraison= fields.Many2one("transport.depot", "Lieu de livraison")
    chargement = fields.Many2one("transport.depot", "Lieu de Chargement")
    product = fields.Many2one("transport.product", "Produit")
    company_id = fields.Many2one('res.company',"Transporteur")

#-----------------DEPENSES-----------------------#
    consogaz_q = fields.Integer("Consomation  Gazoil(L)", )
    consogaz_pu = fields.Integer("PU Gazoil")
    consogaz = fields.Integer("Consomation Gazoil", compute="_amount_gaz")
    road_fees= fields.Integer("Frais de Route")
    bgt=fields.Integer(" Frais Bureau de Gestion Terrestre", help="il s'agit des frais  du Bureau de Terrestre ")
    barc = fields.Integer(" Frais Bureau d'affretement rouitier Centrafricain",
                          help="il s'agit des frais  du  Bureau d'affretement rouitier Centrafricain ")

    douane = fields.Integer("Douane Cachet Corridor")
    fleet_bn = fields.Integer("Bureau National du Fleet")
    lost = fields.Integer("Volume de Coulage en (L)")
    lost_c = fields.Integer("Pu Collage")
    amount_lost = fields.Integer("Montant Collage", compute="_amount_lost")
    total_charges = fields.Integer("Total Charges", compute="_get_total_price")

    state = fields.Selection([('draft', 'Brouillon'),
                              ('validated', 'Valider'),
                              ('cancel', 'Annuler')],
                             string='Etat', default='draft',
                             help="Il s'agit de l'Etat du livre, il peut etre A envoyer, Valider ou Annuler")

    #-------------------------------PV DE RECEPTION-------------------------------------------#

    date_pv = fields.Date("Date de recepion")
    depot_id = fields.Many2one("transport.depot")
    product_r = fields.Many2one("transport.product")
    #ncc = fields.Many2one("fleet.vehicle","Immatriculation Tracteur")
    nbbt = fields.Char("Numero BT")
    ncc = fields.Char("Immatriculation Tracteur")
    distribution = fields.Char("Distribution")
    ntt = fields.Char("No TT")
    nd15 = fields.Char("No D15")
    nbc = fields.Char("No BC SCDP")
    date = fields.Date("Date")
    company_id_pv = fields.Many2one('res.company', "Transporteur")
    file_data = fields.Binary(string="Inserer  le PV ici", attachment=True)  # The field to store the file
    file_name = fields.Char(string="File Name")  # Optional: to store the file's name

    file_bon = fields.Binary(string="Inserer  le Bon ici", attachment=True)  # The field to store the file
    file_nam = fields.Char(string="File Name")  # Optional: to store the file's name

    @api.depends('lost', 'lost_c')
    def _amount_lost(self):
        for record in self:
            record.amount_lost = record.lost * record.lost_c

    @api.depends('quantity','price_unit')
    def _amount_price(self):
        for record in self:
            record.amount = record.quantity * record.price_unit

    @api.depends('consogaz_q', 'consogaz_pu')
    def _amount_gaz(self):
        for record in self:
            record.consogaz = record.consogaz_q * record.consogaz_pu

    @api.depends('consogaz','douane','bgt','barc','consogaz')
    def _get_total_price(self):
        for record in self:
            record.total_charges = record.douane + record.road_fees + record.bgt + record.barc + record.consogaz


    def set_to_draft(self):
        return self.write({'state': 'draft'})

    def set_to_cancel(self):
        return self.write({'state': 'cancel'})

    def set_to_validated(self):
        return self.write({'state': 'validated'})

    @api.model
    def date_format(self, date):
        """Format a date into dd/mm/yy"""
        if date:
            # Convert the Odoo date (string) to a datetime object
            date_obj = dt.strptime(str(date), '%Y-%m-%d')
            # Format it to dd/mm/yy
            formatted_date = date_obj.strftime('%d/%m/%y')
            return formatted_date
        return None

    def send_sms(self):
        vehicule_ids = self.env['fleet.vehicle'].search([])
        driver_ids = self.env['fleet.driver'].search([])
        receiver_ids = self.env['sms.recevier'].search([])
        limit = [14, 7, 3]
        api_key = 'b0l5cGl6TE5JZmt6ZkdIZEZsTUQ='
        url = 'https://app.techsoft-web-agency.com/sms/api'
        senderID = 'YSG'
        # destination = str(self.destination)
        for vehicle in vehicule_ids:
            for piece in vehicle.piece_ids:
                if (piece.date_expi - dt.now().date()).days in limit:
                    for receiver in receiver_ids:
                        message = ' ATTENTION '+str(piece.piece_id.name)+' de la  ' + str(
                            vehicle.license_plate) + ' expire le ' + str(self.date_format(piece.date_expi)) + ' veillez penser à  renouveller.'
                        sms_body = {
                            'action': 'send-sms',
                            'api_key': api_key,
                            'to': '237' + receiver.tel,
                            'from': senderID,
                            'sms': message
                        }
                        final_url = url + "?" + urllib.parse.urlencode(sms_body)
                        requests.get(final_url)

        for driver in driver_ids:
            for piece in driver.piece_ids:
                if (piece.date_expi - dt.now().date()).days in limit:
                    for receiver in receiver_ids:
                        message = ' ATTENTION '+str(piece.piece_id.name)+' du chauffeur  ' + str(
                            driver.partner_id.name) + ' expire le ' + str(self.date_format(piece.date_expi)) + ' veillez penser à  renouveller.'
                        sms_body = {
                            'action': 'send-sms',
                            'api_key': api_key,
                            'to': '237' + receiver.tel,
                            'from': senderID,
                            'sms': message
                        }
                        final_url = url + "?" + urllib.parse.urlencode(sms_body)
                        requests.get(final_url)


class transport_depot(models.Model):
    _name = 'transport.depot'
    _description = "Depot de chargement"

    name = fields.Char("Nom du Depot")
    town = fields.Char("Ville")
    country= fields.Many2one('res.country','Pays')

class transport_produit(models.Model):
    _name = 'transport.product'
    _description = "Produit"

    name = fields.Char("Nom du Produit")

