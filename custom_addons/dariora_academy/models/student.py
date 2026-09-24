from odoo import models, fields


class Student(models.Model):
    _name = "dariora.student"
    _description = "Student"

    name = fields.Char(
        string="Name",
        required=True,
    )

    email = fields.Char(
        string="Email",
        required=True,
    )

    enrollment_ids = fields.One2many(
        "dariora.enrollment",
        "student_id",
        string="Enrollments",
    )
