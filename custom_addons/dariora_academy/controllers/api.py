from odoo import http
from odoo.http import request
import json


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
        "/api/courses",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False,
    )
    def create_course(self):
        try:
            data = json.loads(request.httprequest.data)
        except (ValueError, TypeError):
            return request.make_json_response(
                {"error": "Invalid JSON"},
                status=400,
            )

        # Validation
        if not data.get("name"):
            return request.make_json_response(
                {"error": "name is required"},
                status=400,
            )

        if "price" not in data:
            return request.make_json_response(
                {"error": "price is required"},
                status=400,
            )

        try:
            course = request.env["dariora.course"].sudo().create({
                "name": data.get("name"),
                "description": data.get("description", ""),
                "price": float(data.get("price", 0)),
                "is_published": data.get("is_published", False),
            })

            return request.make_json_response({
                "id": course.id,
                "name": course.name,
                "description": course.description,
                "price": course.price,
                "is_published": course.is_published,
            }, status=201)
        except Exception as e:
            return request.make_json_response(
                {"error": str(e)},
                status=500,
            )

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


