# -*- coding: utf-8 -*-
from odoo import api, fields, models



_JOURS_SEMAINE = [
    ("1","Lundi"),
    ("2","Mardi"),
    ("3","Mercredi"),
    ("4","Jeudi"),
    ("5","Vendredi"),
    ("6","Samedi"),
    ("7","Dimanche"),
]


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('is_date_vente')
    def _compute_date_vente(self):
        for obj in self:
            jour=semaine=mois=annee=False
            if obj.is_date_vente:
                jour = obj.is_date_vente.isoweekday()
                jour = _JOURS_SEMAINE[jour-1][0]
                semaine = obj.is_date_vente.isocalendar()[1]
                mois    = obj.is_date_vente.month
                annee   = str(obj.is_date_vente.year)
            obj.is_jour_vente    = jour
            obj.is_semaine_vente = semaine
            obj.is_mois_vente    = mois
            obj.is_annee_vente   = annee

    is_date_vente    = fields.Date("Date vente")
    is_jour_vente    = fields.Selection(_JOURS_SEMAINE, string="Jour vente", compute=_compute_date_vente, store=True, readonly=True)
    is_semaine_vente = fields.Integer(string="Semaine vente"               , compute=_compute_date_vente, store=True, readonly=True)
    is_mois_vente    = fields.Integer(string="Mois vente"                  , compute=_compute_date_vente, store=True, readonly=True)
    is_annee_vente   = fields.Char(string="Année vente"                 , compute=_compute_date_vente, store=True, readonly=True)



