# ©  2015-2018 Deltatech
# See README.rst file on addons root folder for license details

from odoo import api, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["qty_done"] = vals.get("product_uom_qty")
        return super(StockMoveLine, self).create(vals_list)
