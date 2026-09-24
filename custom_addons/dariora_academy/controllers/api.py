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

    @http.route(
        "/api/courses/<int:course_id>",
        type="http",
        auth="public",
        methods=["PUT"],
        csrf=False,
    )
    def update_course(self, course_id):
        course = request.env["dariora.course"].sudo().browse(course_id)

        if not course.exists():
            return request.make_json_response(
                {"error": "Course not found"},
                status=404,
            )

        try:
            data = json.loads(request.httprequest.data)
        except (ValueError, TypeError):
            return request.make_json_response(
                {"error": "Invalid JSON"},
                status=400,
            )

        # Update only provided fields
        update_data = {}
        if "name" in data:
            update_data["name"] = data["name"]
        if "description" in data:
            update_data["description"] = data["description"]
        if "price" in data:
            update_data["price"] = float(data["price"])
        if "is_published" in data:
            update_data["is_published"] = data["is_published"]

        try:
            course.write(update_data)
            return request.make_json_response({
                "id": course.id,
                "name": course.name,
                "description": course.description,
                "price": course.price,
                "is_published": course.is_published,
            })
        except Exception as e:
            return request.make_json_response(
                {"error": str(e)},
                status=500,
            )

    @http.route(
        "/api/courses/<int:course_id>",
        type="http",
        auth="public",
        methods=["DELETE"],
        csrf=False,
    )
    def delete_course(self, course_id):
        course = request.env["dariora.course"].sudo().browse(course_id)

        if not course.exists():
            return request.make_json_response(
                {"error": "Course not found"},
                status=404,
            )

        try:
            course.unlink()
            return request.make_json_response(
                {"message": "Course deleted successfully"},
                status=200,
            )
        except Exception as e:
            return request.make_json_response(
                {"error": str(e)},
                status=500,
            )
    # Student API

    @http.route(
        "/api/students",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
    )
    def get_students(self):
        students = request.env["dariora.student"].sudo().search([])

        result = []

        for student in students:
            result.append({
                "id": student.id,
                "name": student.name,
                "email": student.email,
            })

        return request.make_json_response(result)

    @http.route(
        "/api/students",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False,
    )
    def create_student(self):
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

        if not data.get("email"):
            return request.make_json_response(
                {"error": "email is required"},
                status=400,
            )

        try:
            student = request.env["dariora.student"].sudo().create({
                "name": data.get("name"),
                "email": data.get("email"),
            })

            return request.make_json_response({
                "id": student.id,
                "name": student.name,
                "email": student.email,
            }, status=201)
        except Exception as e:
            return request.make_json_response(
                {"error": str(e)},
                status=500,
            )

    @http.route(
        "/api/students/<int:student_id>",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
    )
    def get_student(self, student_id):
        student = request.env["dariora.student"].sudo().browse(student_id)

        if not student.exists():
            return request.make_json_response(
                {"error": "Student not found"},
                status=404,
            )

        return request.make_json_response({
            "id": student.id,
            "name": student.name,
            "email": student.email,
        })

    @http.route(
        "/api/students/<int:student_id>",
        type="http",
        auth="public",
        methods=["PUT"],
        csrf=False,
    )
    def update_student(self, student_id):
        student = request.env["dariora.student"].sudo().browse(student_id)

        if not student.exists():
            return request.make_json_response(
                {"error": "Student not found"},
                status=404,
            )

        try:
            data = json.loads(request.httprequest.data)
        except (ValueError, TypeError):
            return request.make_json_response(
                {"error": "Invalid JSON"},
                status=400,
            )

        # Update only provided fields
        update_data = {}
        if "name" in data:
            update_data["name"] = data["name"]
        if "email" in data:
            update_data["email"] = data["email"]

        try:
            student.write(update_data)
            return request.make_json_response({
                "id": student.id,
                "name": student.name,
                "email": student.email,
            })
        except Exception as e:
            return request.make_json_response(
                {"error": str(e)},
                status=500,
            )

    @http.route(
        "/api/students/<int:student_id>",
        type="http",
        auth="public",
        methods=["DELETE"],
        csrf=False,
    )
    def delete_student(self, student_id):
        student = request.env["dariora.student"].sudo().browse(student_id)

        if not student.exists():
            return request.make_json_response(
                {"error": "Student not found"},
                status=404,
            )

        try:
            student.unlink()
            return request.make_json_response(
                {"message": "Student deleted successfully"},
                status=200,
            )
        except Exception as e:
            return request.make_json_response(
                {"error": str(e)},
                status=500,
            )
