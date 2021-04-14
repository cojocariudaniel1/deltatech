# ©  2015-2019 Deltatech
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

{
    "name": "MRP Parameter",
    "version": "12.0.1.0.0",
    "author": "Terrabit, Dorin Hongu",
    "website": "https://www.terrabit.ro",
    "license": "LGPL-3",
    "category": "Manufacturing",
    "depends": ["mrp", "product"],
    "data": [
        "views/mrp_parameter_view.xml",
        "views/mrp_workcenter_view.xml",
        "views/mrp_routing_view.xml",
        "views/mrp_workorder_view.xml",
        "views/product_view.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "images": [],
    "development_status": "stable",
    "maintainers": ["dhongu"],
}
