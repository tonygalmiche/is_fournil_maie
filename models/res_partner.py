# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_num_client = fields.Char("N°client chez le fournsseur")
