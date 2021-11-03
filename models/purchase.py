# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import Warning


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        for obj in self:
            companies = self.env['res.company'].sudo().search([])
            company=False
            for c in companies:
                if c.partner_id==obj.partner_id:
                    company=c
            if company:
                if obj.partner_ref:
                    raise Warning('Une commande client a déjà été générée => Nouvelle validation impossible !')
                warehouse = self.env['stock.warehouse'].sudo().search([('company_id','=',company.id)])[0]
                lines=[]
                for line in obj.order_line:
                    vals={
                        'product_id'     : line.product_id.id, 
                        'name'           : line.name, 
                        'product_uom_qty': line.product_qty,
                        'price_unit'     : line.price_unit,
                    }
                    lines.append([0,False,vals])
                vals = {
                    'partner_id': obj.company_id.partner_id.id,
                    'client_order_ref': obj.name,
                    'order_line': lines,
                    'picking_policy': 'direct',
                    'company_id': company.id,
                    'warehouse_id':warehouse.id,
                    'invoice_status': 'to invoice',
                    'commitment_date': obj.date_planned,
                    'team_id': obj.company_id.partner_id.team_id.id,

                }
                order = self.env['sale.order'].sudo().create(vals)
                obj.partner_ref = order.name
        return super(PurchaseOrder, self).button_confirm()

