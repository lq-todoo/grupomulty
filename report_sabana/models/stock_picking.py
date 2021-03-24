# -*- coding: utf-8 -*-
from odoo import models,fields,api,_

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    total_weigth = fields.Float('Total Weigth',compute="_compute_total_weigth",store=True)
    
    def update_action_assign(self):
        self.action_assign()
        for record in self.move_line_ids_without_package:
            record.qty_done = record.product_uom_qty
            
    @api.depends('move_ids_without_package.weigth')
    def _compute_total_weigth(self):
        weigth = 0
        for record in self.move_ids_without_package:
            if record.product_id:
                if record.weigth != 0:
                    weigth += record.weigth 
                    self.write({'total_weigth':weigth})
                else:
                    self.total_weigth = 0
            else:
                self.total_weigth = 0
                

class StockMove(models.Model):
    _inherit = 'stock.move'
    
    weigth = fields.Float('Weigth',store=True)
    
    @api.onchange('product_id','qty_done')
    def _onchange_partner_id(self):
        for record in self:
            record.weigth = 0
            if record.product_id:
                record.weigth = record.product_id.weight * record.qty_done