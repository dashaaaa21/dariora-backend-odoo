{
    "name": "Dariora Academy",
    "version": "1.0.0",
    "summary": "Backend for Dariora Academy",
    "description": """
        Dariora Academy backend module.

        This module will manage:
        - Courses
        - Students
        - Lessons
        - Enrollments
    """,
    "category": "Education",
    "author": "Dariora Academy",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/course_views.xml",
    ],
    "installable": True,
    "application": True,
}