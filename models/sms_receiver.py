#-*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
import urllib, requests
from datetime import datetime as dt

class sms_receiver(models.Model):
    _name = 'sms.recevier'
    _description = 'Recepteur de SMS'
    _rec_name='partner_id'

    partner_id = fields.Many2one('res.partner')
    tel= fields.Char("Numero de Telephone")

    def send_sms(self):
        vehicule_ids = self.env['fleet.vehicule'].search([])
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
                        message = "ATTENTION", +str(piece.piece_id.name) + " Du vehicule" + str(vehicle.car_id.license_plate) + "expire le " \
                          + str(dt.strptime(str(piece.date_expi), '%d-%m-%Y')) + "Veillez penser à la renouveller !!"

                        sms_body = {
                            'action': 'send-sms',
                            'api_key': api_key,
                            'to': '237'+receiver.tel,
                            'from': senderID,
                            'sms': message
                        }
                        final_url = url + "?" + urllib.parse.urlencode(sms_body)
                        requests.get(final_url)


