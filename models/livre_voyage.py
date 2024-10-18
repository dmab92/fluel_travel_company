#-*- coding: utf-8 -*-
import time
from odoo import models, fields, api

class livre_voyage(models.Model):
    _name = 'livre.voyage'
    _description = "Bon Livre de Voyage"
    __rec_name ='number'


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

    number = fields.Char("Voyage No", readonly="True", default=lambda self: self._get_next_reference())

    name = fields.Char("Bon d'enlevement No")
    #date_register = fields.Date("Date d'enregitrement")
    date_bon = fields.Date("Date du bon d'enlevement")
    client = fields.Many2one("res.partner", "Client")
    quantity = fields.Integer("Quantite")
    price_unit = fields.Integer("Pu")
    amount = fields.Integer("Montant Transport Carburant", compute="_amount_price",
                            help="Il s'agit du montant du transort du carbutant, quantite * pu",
                            )
    fleet = fields.Many2one("fleet.vehicle","Immatriculation Remorque")
    driver= fields.Many2one('res.partner','Chauffeur')
    livraison= fields.Many2one("transport.depot", "Lieu de livraison")
    chargement = fields.Many2one("transport.depot", "Lieu de Chargement")
    product = fields.Many2one("transport.product", "Produit")
    company_id = fields.Many2one('res.company',"Transporteur")

    #file_bon_ids = fields.Many2many('ir.attachment', string='Inserer  le bon ici')



#-----------------DEPENSES-----------------------#
    consogaz_q = fields.Integer("Consomation  Gazoil(L)", )
    consogaz_pu = fields.Integer("PU Gazoil")
    consogaz = fields.Integer("Consomation Gazoil", compute="_amount_gaz")
    road_fees= fields.Integer("Frais de Route")
    bgt=fields.Integer(" Frais Bureau de Gestion Terrestre", help="il s'agit des frais  du Bureau de Terrestre ")
    barc = fields.Integer(" Frais Bureau d'affretement rouitier Centrafricain",
                          help="il s'agit des frais  du  Bureau d'affretement rouitier Centrafricain ")

    douane = fields.Integer("Douane Cachet Corridor")
    lost = fields.Integer("Volume de Collage en (L)")
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

    #file_pv_ids = fields.Many2many('ir.attachment', string='Inserer  le PV ici')

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


class transport_depot(models.Model):
    _name = 'transport.depot'
    _description = "Depot de chargement"

    name = fields.Char("Nom du Depot")
    town = fields.Char("Ville")
    country= fields.Many2one('res.country','Pays')

class transport_produit(models.Model):
    _name = 'transport.product'
    _description = "Produit"

    name = fields.Char("Nom du Depot")
