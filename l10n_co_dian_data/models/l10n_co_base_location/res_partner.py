# Copyright 2016 Nicolas Bessi, Camptocamp SA
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = "res.partner"

    zip_id = fields.Many2one("res.city.zip", "ZIP Location")
    country_code = fields.Char(related='country_id.code', store=False)

    @api.onchange("city_id")
    def _onchange_city_id(self):
        if not self.zip_id:
            super()._onchange_city_id()
        if self.zip_id and self.city_id != self.zip_id.city_id:
            self.update({"zip_id": False, "zip": False, "city": False})
        if self.city_id and self.country_enforce_cities:
            return {"domain": {"zip_id": [("city_id", "=", self.city_id.id)]}}
        return {"domain": {"zip_id": []}}

    @api.onchange("country_id")
    def _onchange_country_id(self):
        res = super()._onchange_country_id()
        if self.zip_id and self.zip_id.city_id.country_id != self.country_id:
            self.zip_id = False
        return res

    @api.onchange("zip_id")
    def _onchange_zip_id(self):
        if self.zip_id:
            vals = {
                "city_id": self.zip_id.city_id,
                "zip": self.zip_id.name,
                "city": self.zip_id.city_id.name,
            }
            if self.zip_id.city_id.country_id:
                vals.update({"country_id": self.zip_id.city_id.country_id})
            if self.zip_id.city_id.state_id:
                vals.update({"state_id": self.zip_id.city_id.state_id})
            self.update(vals)
        elif not self.country_enforce_cities:
            self.city_id = False


    @api.constrains("zip_id", "country_id", "city_id", "state_id")
    def _check_zip(self):
        if self.env.context.get("skip_check_zip"):
            return
        for rec in self:
            if not rec.zip_id:
                continue
            _logger.info('checkzip')

            _logger.info(rec.state_id)
            zip_model = self.env['res.city.zip'].search([('id','=', rec.zip_id.id)])
            #zipid = zip_model.search('id','=', rec.zip_id.id)
            _logger.info(zip_model)
            _logger.info(zip_model.city_id.state_id.id)
            _logger.info(rec.state_id.id)
            _logger.info(zip_model.city_id)
            _logger.info(rec.city_id)
            _logger.info(zip_model.city_id.country_id.id)
            _logger.info(rec.country_id.id)


            if int(zip_model.city_id.state_id.id) != int(rec.state_id.id):
                raise ValidationError(
                    _("The state of the partner %s differs from that in " "location %s")
                    % (rec.name, zip_model.name)
                )
            if int(zip_model.city_id.country_id.id) != int(rec.country_id.id):
                raise ValidationError(
                    _(
                        "The country of the partner %s differs from that in "
                        "location %s"
                    )
                    % (rec.name, zip_model.name)
                )
            if rec.type != 'contact' and zip_model.city_id != rec.city_id:
                raise ValidationError(
                    _("The city of partner %s differs from that in " "location %s")
                    % (rec.name, zip_model.name)
                )
            _logger.info('full')


    @api.onchange("state_id")
    def _onchange_state_id(self):
        vals = {}
        if self.state_id.country_id:
            vals.update({"country_id": self.state_id.country_id})
        if self.zip_id and self.state_id != self.zip_id.city_id.state_id:
            vals.update({"zip_id": False, "zip": False, "city": False})
        self.update(vals)
