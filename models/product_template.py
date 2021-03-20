# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from random import randint


class IsFamille(models.Model):
    _name = 'is.famille'
    _description = "Famille"

    name  = fields.Char("Famille", required=True)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_allergene_ids = fields.Many2many('is.allergene', 'product_template_allergene_rel', 'product_id', 'allergene_id', 'Allergènes')
    is_famille_id    = fields.Many2one('is.famille', string='Famille')
    is_nb_jours_dluo = fields.Integer('Nb jours DLUO')


    def bom_multiniveaux(self,bom):
        for line in bom.bom_line_ids:
            boms = self.env['mrp.bom'].search([('product_tmpl_id','=',line.product_id.id)])
            if len(boms)>0:
                for bom in boms:
                    self.bom_multiniveaux(bom)
            else:
                print(bom.product_tmpl_id.is_allergene_ids,line.product_id.is_allergene_ids)
                
              
    @api.model
    def _rechercher_allergenes_ir_cron(self):
        boms = self.env['mrp.bom'].search([])
        for bom in boms:
            bom.product_tmpl_id.is_allergene_ids=False

        for bom in boms:
            #print(bom.product_tmpl_id.name)
            self.bom_multiniveaux(bom)
            #for line in bom.bom_line_ids:
            #    print('- ',line.product_id.name)
        return True


class IsAllergene(models.Model):
    _name = 'is.allergene'
    _description = "Allergène"


    def _get_default_color(self):
        return randint(1, 11)

    name  = fields.Char("Allergène", required=True)
    color = fields.Integer(string='Color Index', default=_get_default_color)

