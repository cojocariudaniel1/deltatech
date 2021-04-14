# ©  2015-2020 Deltatech
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details


import werkzeug

from odoo import api, models, tools


class ProductImage(models.Model):
    _inherit = "product.image"

    @api.onchange("name")
    def onchange_name(self):
        parsed_url = werkzeug.urls.url_parse(self.name)
        if parsed_url.scheme:
            data = self.product_tmpl_id.load_image_from_url(self.name)
            if data:
                self.name = self.name.split("/")[-1]
                vals = {"image": data}
                tools.image_resize_images(vals)
                self.image = vals["image"]
                self.image_medium = vals["image_medium"]

    def write(self, vals):
        if "name" in vals:
            image_file_name = vals["name"]
            parsed_url = werkzeug.urls.url_parse(image_file_name)
            if parsed_url.scheme:
                data = self.product_tmpl_id.load_image_from_url(image_file_name)
                if data:
                    vals["name"] = image_file_name.split("/")[-1]
                    vals["image"] = data
                    tools.image_resize_images(vals)
        return super(ProductImage, self).write(vals)
