from odoo import models, fields


class Enrollment(models.Model):
    _name = "dariora.enrollment"
    _description = "Dariora Academy Enrollment"

    student_id = fields.Many2one(
        "dariora.student",
        string="Student",
        required=True,
    )

    course_id = fields.Many2one(
        "dariora.course",
        string="Course",
        required=True,
    )

    enrollment_date = fields.Date(
        string="Enrollment Date",
        default=fields.Date.today,
    )

    status = fields.Selection(
        [
            ("active", "Active"),
            ("completed", "Completed"),
        ],
        string="Status",
        default="active",
    )
