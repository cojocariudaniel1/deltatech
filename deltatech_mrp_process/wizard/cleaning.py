# ©  2015-2018 Deltatech
# See README.rst file on addons root folder for license details


from odoo import api, fields, models


class MRPCleaning(models.TransientModel):
    _name = "mrp.cleaning"
    _description = "MRP Cleaning"

    cleaning_date = fields.Date()
    cleaning_note = fields.Text()
    workcenter_id = fields.Many2one("mrp.workcenter")

    @api.model
    def default_get(self, fields_list):
        default = super(MRPCleaning, self).default_get(fields_list)

        workcenter = self.env["mrp.workcenter"].browse(self.env.context.get("active_id"))
        default["workcenter_id"] = workcenter.id
        default["cleaning_date"] = workcenter.cleaning_date
        default["cleaning_note"] = workcenter.cleaning_note
        return default

    @api.multi
    def do_save(self):
        self.workcenter_id.write({"cleaning_date": self.cleaning_date, "cleaning_note": self.cleaning_note})
