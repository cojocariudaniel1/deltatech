# ©  2015-2020 Deltatech
# See README.rst file on addons root folder for license details


from odoo import _, api, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # # pretul de achizitie in moneda documentului
    # todo: de actualizat acest pret cu valaorea produsului in momentul livarii
    # oare de ce il fac camp caclulat ?
    # purchase_price = fields.Float(string='Cost Price', digits=dp.get_precision('Product Price'),
    #                               compute="_compute_purchase_price", store=True)

    @api.depends("product_id")
    def _compute_purchase_price(self):
        for line in self:
            line.purchase_price = line._compute_margin(line.order_id, line.product_id, line.product_uom)

    def change_price_or_product(self, res):
        if not res.get("warning", False):
            if self.price_unit < self.purchase_price and self.purchase_price > 0:
                warning = {
                    "title": _("Price Error!"),
                    "message": _("Do not sell below the purchase price."),
                }
                res["warning"] = warning
            # if not self.price_unit:
            #     warning = {
            #         'title': _('Price Error!'),
            #         'message': _('Do not sell without price.'),
            #     }
            #     res['warning'] = warning
        return res

    @api.onchange("product_id")
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        res = self.change_price_or_product(res)
        return res

    @api.onchange("price_unit")
    def price_unit_change(self):
        res = {}
        res = self.change_price_or_product(res)
        return res

    # @api.multi
    # @api.onchange('price_unit')
    # def price_unit_change(self):
    #     res = {}
    #
    #     if self.price_unit < self.purchase_price and self.purchase_price > 0:
    #         warning = {
    #             'title': _('Price Error!'),
    #             'message': _('You can not sell below the purchase price.'),
    #         }
    #         res['warning'] = warning
    #     return res

    @api.one
    @api.constrains("price_unit", "purchase_price")
    def _check_sale_price(self):
        if self.price_unit == 0:
            if not self.env["res.users"].has_group("deltatech_sale_margin.group_sale_below_purchase_price"):
                raise UserError(_("You can not sell without price."))
            else:
                message = _("Sale %s without price.") % self.product_id.name
                self.order_id.message_post(body=message)

        if self.price_unit < self.purchase_price:
            if not self.env["res.users"].has_group("deltatech_sale_margin.group_sale_below_purchase_price"):
                raise UserError(_("You can not sell below the purchase price."))
            else:
                message = _("Sale %s under the purchase price.") % self.product_id.name
                self.order_id.message_post(body=message)

    # @api.multi
    # def write(self, vals):
    #     super(sale_order_line, self).write(vals)
    #     if vals.get('price_unit', False):
    #         for line in self:
    #             if vals.get('price_unit', 0) < self.purchase_price and self.purchase_price > 0:
    #                 message = _('Sale under the purchase price.')
    #                 line.order_id.message_post(body=message)
