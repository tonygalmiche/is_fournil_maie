# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.depends('is_nb_clients','amount_total')
    def _compute_is_panier_moyen(self):
        for obj in self:
            print(obj)
            panier=False
            if obj.is_nb_clients>0:
                panier = obj.amount_total/obj.is_nb_clients
            obj.is_panier_moyen=panier

    is_nb_clients   = fields.Integer("Nombre de clients")
    is_panier_moyen = fields.Float(string="Panier moyen", compute=_compute_is_panier_moyen, store=True, readonly=True)

