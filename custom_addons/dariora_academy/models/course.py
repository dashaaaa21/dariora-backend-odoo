from odoo import models, fields


class Course(models.Model):
    _name = "dariora.course"
    _description = "Dariora Academy Course"

    name = fields.Char(
        string="Course Name",
        required=True,
    )

    description = fields.Text(
        string="Description",
    )

    price = fields.Float(
        string="Price",
    )

    is_published = fields.Boolean(
        string="Published",
        default=False,
    )