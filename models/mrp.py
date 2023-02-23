# -*- coding: utf-8 -*-
from odoo import fields, models, api
from datetime import timedelta

class MrpBom(models.Model):
    _inherit = "mrp.bom"

    is_mode_operatoire = fields.Text(string="Mode opératoire")



class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.depends('date_planned_start','product_id')
    def _compute_is_dluo(self):
        for obj in self:
            obj.is_dluo = obj.date_planned_start + timedelta(days=obj.product_id.is_nb_jours_dluo)
          
    is_dluo = fields.Date("DLUO", compute=_compute_is_dluo, store=False, readonly=True)



