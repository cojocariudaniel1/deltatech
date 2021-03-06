# ©  2008-2021 Deltatech
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details


from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    init_value = fields.Float(string="Initial value")
    first_revaluation = fields.Date(string="First Revaluation")

    def view_revaluation(self):
        action = self.env.ref("deltatech_stock_revaluation.action_stock_revaluation_line").read()[0]
        action["domain"] = "[('quant_id','in',[" + ",".join(map(str, self.ids)) + "])]"
        return action
