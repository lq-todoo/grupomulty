# -*- coding: utf-8 -*-
import logging
from odoo import fields, models, api,_

_logger = logging.getLogger(__name__)

    
class AccountMove(models.Model):
    _inherit = 'account.move'
    
    total_weigth = fields.Float('Total Weigth',store=True)
    total_weigth_1 = fields.Float('Total Weigth',compute="_compute_total_weigth_1")
    pricelist = fields.Char('Pricelist',store=True)
    partner_deal_id = fields.Many2one('res.partner.deal',"Deal Name",store=True)
    partner_deal_id_1 = fields.Many2one('res.partner.deal',"Deal Name",store=True,related="partner_id.partner_deal_id")
    
    @api.depends('invoice_line_ids.weigth')
    def _compute_total_weigth_1(self):
        weigth = 0
        for record in self.invoice_line_ids:
            if record.product_id:
                if record.weigth != 0:
                    weigth += record.weigth 
                    self.write({'total_weigth_1':weigth})
                else:
                    self.total_weigth_1 = 0
            else:
                self.total_weigth_1 = 0
    
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    weigth = fields.Float('Weigth',store=True)
