#-*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
# import urllib, requests
# from datetime import datetime as dt

class RepairOrder(models.Model):
    _inherit = 'repair.order'

    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle', required=True)
    total_amount = fields.Integer("Main d'Oeuvre en FCFA")

    # @api.depends('quantity','price_unit')
    # def _total_amount(self):
    #     for record in self:
    #         record.total_amount = sum(record.mapped('amount_residual_signed'))