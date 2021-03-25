# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from random import randint


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"


    @api.model
    def create(self, vals):
        if 'stop_write_recursion' not in self.env.context:
            if "product_id" in vals:
                product_id = vals["product_id"]
                current_company_id = self.env.context.get('allowed_company_ids')[0]
                companies = self.env['res.company'].sudo().search([('parent_id','=',False)])
                for c in companies:
                    if c.id==current_company_id:
                        lines = self.env['res.company'].sudo().search([('parent_id','=',c.id)])
                        for line in lines:
                            products = self.env['product.product'].sudo().search([('id','=',product_id),('company_id','=',False)])
                            for product in products:
                                orderpoints=self.env['stock.warehouse.orderpoint'].sudo().search([('product_id','=',product_id),('company_id','=',line.id)])
                                if not orderpoints:
                                    warehouse = self.env['stock.warehouse'].sudo().search([('id','=',line.id)])[0]
                                    v={
                                        "warehouse_id"   : warehouse.id,
                                        "location_id"    : warehouse.lot_stock_id.id,
                                        "product_id"     : product.id,
                                        "company_id"     : line.id,
                                        "product_min_qty": vals["product_min_qty"],
                                        "product_max_qty": vals["product_max_qty"],
                                        "qty_multiple"   : vals["qty_multiple"],
                                    }
                                    r=self.with_context(stop_write_recursion=1).env['stock.warehouse.orderpoint'].sudo().create(v)
        res = super(StockWarehouseOrderpoint, self).create(vals)
        return res


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

