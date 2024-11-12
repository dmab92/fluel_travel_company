#-*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
# import urllib, requests
# from datetime import datetime as dt

class RepairOrder(models.Model):
    _inherit = 'repair.order'

    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle', required=True)
    total_amount = fields.Integer("Main d'Oeuvre en FCFA")
    company_id = fields.Many2one('res.company', string='Sociéte')
    total_amount = fields.Float(string="Total Amount", compute='_compute_total_amount', store=True)
    odometer = fields.Float("Dernier Kilometrage",related='vehicle_id.odometer')
    @api.depends('move_ids.product_price')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(move.product_price for move in record.move_ids)

class StockMove(models.Model):
    _inherit = 'stock.move'

    product_price = fields.Float(string="Prix  ", readonly=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for move in self:
            if move.product_id:
                move.product_price = move.product_id.lst_price * move.product_uom_qty
            else:
                move.product_price = 0.0

    # @api.depends('quantity','price_unit')
    # def _total_amount(self):
    #     for record in self:
    #         record.total_amount = sum(record.mapped('amount_residual_signed'))