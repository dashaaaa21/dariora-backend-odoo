from odoo import http
from odoo.http import request


class DarioraAcademyAPI(http.Controller):

    @http.route(
        "/api/courses",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
    )
    def get_courses(self):
        courses = request.env["dariora.course"].sudo().search([])

        result = []

        for course in courses:
            result.append({
                "id": course.id,
                "name": course.name,
                "description": course.description,
                "price": course.price,
                "is_published": course.is_published,
            })

        return request.make_json_response(result)

    @http.route(
        "/api/courses/<int:course_id>",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
    )
    def get_course(self, course_id):
        course = request.env["dariora.course"].sudo().browse(course_id)

        if not course.exists():
            return request.make_json_response(
                {"error": "Course not found"},
                status=404,
            )

        return request.make_json_response({
            "id": course.id,
            "name": course.name,
            "description": course.description,
            "price": course.price,
            "is_published": course.is_published,
        })

