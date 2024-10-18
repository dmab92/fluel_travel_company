# -*- coding: utf-8 -*-
# from odoo import http


# class TransportApp(http.Controller):
#     @http.route('/transport_app/transport_app', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/transport_app/transport_app/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('transport_app.listing', {
#             'root': '/transport_app/transport_app',
#             'objects': http.request.env['transport_app.transport_app'].search([]),
#         })

#     @http.route('/transport_app/transport_app/objects/<model("transport_app.transport_app"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('transport_app.object', {
#             'object': obj
#         })

