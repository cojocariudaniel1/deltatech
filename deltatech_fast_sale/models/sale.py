# ©  2015-2018 Deltatech
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details


from odoo import api, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_button_confirm_to_invoice(self):

        if self.state in ["draft", "sent"]:
            self.action_confirm()  # confirma comanda

        for picking in self.picking_ids:
            if picking.state not in ["done", "cancel"]:
                picking.action_assign()  # verifica disponibilitate
                if not all(move.state == "assigned" for move in picking.move_lines):
                    raise UserError(_("Not all products are available."))

                for move_line in picking.move_lines:
                    if move_line.product_uom_qty > 0 and move_line.quantity_done == 0:
                        move_line.write({"quantity_done": move_line.product_uom_qty})
                    else:
                        move_line.unlink()
                picking.with_context(force_period_date=self.date_order).action_done()

        if self.fiscal_position_id:
            action_obj = self.env.ref("sale.action_view_sale_advance_payment_inv")
            action = action_obj.read()[0]
            action["context"] = {"force_period_date": self.date_order}
            return action
        else:
            wizard = self.env["sale.advance.payment.inv"].with_context(active_ids=self.ids, open_invoices=True)
            defaults = wizard.default_get(["advance_payment_method", "product_id", "deposit_account_id"])
            wizard = wizard.new(defaults)
            return wizard.create_invoices()

    # data in factura trebuie sa fie data curenta nu data cand a fost facuta comanda de vanzare
    # @api.multi
    # def _prepare_invoice(self):
    #     invoice_vals = super(sale_order, self)._prepare_invoice()
    #     invoice_vals['date_invoice'] = self.date_order.date()
    #     return invoice_vals

    @api.multi
    def action_button_confirm_notice(self):

        picking_ids = self.env["stock.picking"]
        for picking in self.picking_ids:
            if picking.state == "assigned":
                picking.write({"notice": True})
                picking_ids |= picking

        if not picking_ids:
            return

        action = self.env.ref("stock.action_picking_tree")
        result = action.read()[0]

        result["context"] = {}

        pick_ids = picking_ids.ids
        # choose the view_mode accordingly
        if len(pick_ids) > 1:
            result["domain"] = "[('id','in',%s)]" % pick_ids.ids
        elif len(pick_ids) == 1:
            res = self.env.ref("stock.view_picking_form", False)
            result["views"] = [(res and res.id or False, "form")]
            result["res_id"] = picking_ids.id
        return result
