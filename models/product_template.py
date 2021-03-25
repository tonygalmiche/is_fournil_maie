# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from random import randint




# fournil-maie=# select id,name,company_id,lot_stock_id from stock_warehouse;
#  id |                   name                    | company_id | lot_stock_id 
# ----+-------------------------------------------+------------+--------------
#   1 | San Francisco                             |          1 |            8
#   4 | MACPAIN (centre de production et magasin) |          4 |           48
#   5 | MPJ Developpement (holding) (I)           |          5 |           60
#   3 | MPJ CHAPEAU ROUGE (magasin) (II)          |          3 |           36
#   2 | MPJ FAIDHERBE                             |          2 |           24
# (5 lignes)

# fournil-maie=# \q
# odoo@buster:/$ echo "select id,name,trigger,warehouse_id,location_id,product_id,product_category_id,product_min_qty,product_max_qty,qty_multiple,company_id,qty_to_order from stock_warehouse_orderpoint where product_id=1731" | psql fournil-maie
#  id  |   name   | trigger | warehouse_id | location_id | product_id | product_category_id | product_min_qty | product_max_qty | qty_multiple | company_id | qty_to_order 
# -----+----------+---------+--------------+-------------+------------+---------------------+-----------------+-----------------+--------------+------------+--------------
#  119 | OP/00018 | auto    |            5 |          60 |       1731 |                   1 |         10.0000 |         20.0000 |      30.0000 |          5 |           30
#  120 | OP/00019 | auto    |            4 |          48 |       1731 |                   1 |         11.0000 |         21.0000 |       1.0000 |          4 |           21
# (2 lignes)






class IsFamille(models.Model):
    _name = 'is.famille'
    _description = "Famille"

    name  = fields.Char("Famille", required=True)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_allergene_ids = fields.Many2many('is.allergene', 'product_template_allergene_rel', 'product_id', 'allergene_id', 'Allergènes')
    is_famille_id    = fields.Many2one('is.famille', string='Famille')
    is_nb_jours_dluo = fields.Integer('Nb jours DLUO')


    def bom_multiniveaux(self, bom, compose_id, level):
        if level>20:
            return
        boms = self.env['mrp.bom'].search([('product_tmpl_id','=',compose_id.id)])
        if boms:
            for b in boms:
                for line in b.bom_line_ids:
                    self.bom_multiniveaux(bom,line.product_id.product_tmpl_id,level+1)
        else:
            ids=[]
            for x in bom.product_tmpl_id.is_allergene_ids:
                ids.append(x.id)
            for l in compose_id.is_allergene_ids:
                if l.id not in ids:
                    ids.append(l.id)
            bom.product_tmpl_id.is_allergene_ids = [(6, 0, ids)]


    @api.model
    def _rechercher_allergenes_ir_cron(self):
        boms = self.env['mrp.bom'].search([])
        for bom in boms:
            bom.product_tmpl_id.is_allergene_ids=False
            self.bom_multiniveaux(bom,bom.product_tmpl_id,1)
        return True


class IsAllergene(models.Model):
    _name = 'is.allergene'
    _description = "Allergène"


    def _get_default_color(self):
        return randint(1, 11)

    name  = fields.Char("Allergène", required=True)
    color = fields.Integer(string='Color Index', default=_get_default_color)

