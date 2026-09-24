from odoo import http
from odoo.http import request
import json


def cors_response(data, status=200, headers=None):
    """Create JSON response with CORS headers"""
    response = request.make_json_response(data, status=status, headers=headers)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Max-Age'] = '3600'
    return response


class DarioraAcademyAPI(http.Controller):

    # CORS Preflight for Courses
    @http.route(
        "/api/courses",
        type="http",
        auth="public",
        methods=["OPTIONS"],
        csrf=False,
    )
    def options_courses(self):
        return cors_response({})

    @http.route(
        "/api/courses/<int:course_id>",
        type="http",
        auth="public",
        methods=["OPTIONS"],
        csrf=False,
    )
    def options_course_id(self, course_id):
        return cors_response({})

    # CORS Preflight for Students
    @http.route(
        "/api/students",
        type="http",
        auth="public",
        methods=["OPTIONS"],
        csrf=False,
    )
    def options_students(self):
        return cors_response({})

    @http.route(
        "/api/students/<int:student_id>",
        type="http",
        auth="public",
        methods=["OPTIONS"],
        csrf=False,
    )
    def options_student_id(self, student_id):
        return cors_response({})

    # CORS Preflight for Enrollments
    @http.route(
        "/api/enrollments",
        type="http",
        auth="public",
        methods=["OPTIONS"],
        csrf=False,
    )
    def options_enrollments(self):
        return cors_response({})

    @http.route(
        "/api/enrollments/<int:enrollment_id>",
        type="http",
        auth="public",
        methods=["OPTIONS"],
        csrf=False,
    )
    def options_enrollment_id(self, enrollment_id):
        return cors_response({})

    # COURSES

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

        return cors_response(result)

    @http.route(
        "/api/courses",
        type="http",
        auth="user",
        methods=["POST"],
        csrf=False,
    )
    def create_course(self):
        try:
            data = json.loads(request.httprequest.data)
        except (ValueError, TypeError):
            return cors_response(
                {"error": "Invalid JSON"},
                status=400,
            )

        # Validation
        if not data.get("name"):
            return cors_response(
                {"error": "name is required"},
                status=400,
            )

        if "price" not in data:
            return cors_response(
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

            return cors_response({
                "id": course.id,
                "name": course.name,
                "description": course.description,
                "price": course.price,
                "is_published": course.is_published,
            }, status=201)
        except Exception as e:
            return cors_response(
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
            return cors_response(
                {"error": "Course not found"},
                status=404,
            )

        return cors_response({
            "id": course.id,
            "name": course.name,
            "description": course.description,
            "price": course.price,
            "is_published": course.is_published,
        })

    @http.route(
        "/api/courses/<int:course_id>",
        type="http",
        auth="user",
        methods=["PUT"],
        csrf=False,
    )
    def update_course(self, course_id):
        course = request.env["dariora.course"].sudo().browse(course_id)

        if not course.exists():
            return cors_response(
                {"error": "Course not found"},
                status=404,
            )

        try:
            data = json.loads(request.httprequest.data)
        except (ValueError, TypeError):
            return cors_response(
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
            return cors_response({
                "id": course.id,
                "name": course.name,
                "description": course.description,
                "price": course.price,
                "is_published": course.is_published,
            })
        except Exception as e:
            return cors_response(
                {"error": str(e)},
                status=500,
            )

    @http.route(
        "/api/courses/<int:course_id>",
        type="http",
        auth="user",
        methods=["DELETE"],
        csrf=False,
    )
    def delete_course(self, course_id):
        course = request.env["dariora.course"].sudo().browse(course_id)

        if not course.exists():
            return cors_response(
                {"error": "Course not found"},
                status=404,
            )

        try:
            course.unlink()
            return cors_response(
                {"message": "Course deleted successfully"},
                status=200,
            )
        except Exception as e:
            return cors_response(
                {"error": str(e)},
                status=500,
            )
    # Student API

    @http.route(
        "/api/students",
        type="http",
        auth="user",
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

        return cors_response(result)

    @http.route(
        "/api/students",
        type="http",
        auth="user",
        methods=["POST"],
        csrf=False,
    )
    def create_student(self):
        try:
            data = json.loads(request.httprequest.data)
        except (ValueError, TypeError):
            return cors_response(
                {"error": "Invalid JSON"},
                status=400,
            )

        # Validation
        if not data.get("name"):
            return cors_response(
                {"error": "name is required"},
                status=400,
            )

        if not data.get("email"):
            return cors_response(
                {"error": "email is required"},
                status=400,
            )

        try:
            student = request.env["dariora.student"].sudo().create({
                "name": data.get("name"),
                "email": data.get("email"),
            })

            return cors_response({
                "id": student.id,
                "name": student.name,
                "email": student.email,
            }, status=201)
        except Exception as e:
            return cors_response(
                {"error": str(e)},
                status=500,
            )

    @http.route(
        "/api/students/<int:student_id>",
        type="http",
        auth="user",
        methods=["GET"],
        csrf=False,
    )
    def get_student(self, student_id):
        student = request.env["dariora.student"].sudo().browse(student_id)

        if not student.exists():
            return cors_response(
                {"error": "Student not found"},
                status=404,
            )

        return cors_response({
            "id": student.id,
            "name": student.name,
            "email": student.email,
        })

    @http.route(
        "/api/students/<int:student_id>",
        type="http",
        auth="user",
        methods=["PUT"],
        csrf=False,
    )
    def update_student(self, student_id):
        student = request.env["dariora.student"].sudo().browse(student_id)

        if not student.exists():
            return cors_response(
                {"error": "Student not found"},
                status=404,
            )

        try:
            data = json.loads(request.httprequest.data)
        except (ValueError, TypeError):
            return cors_response(
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
            return cors_response({
                "id": student.id,
                "name": student.name,
                "email": student.email,
            })
        except Exception as e:
            return cors_response(
                {"error": str(e)},
                status=500,
            )

    @http.route(
        "/api/students/<int:student_id>",
        type="http",
        auth="user",
        methods=["DELETE"],
        csrf=False,
    )
    def delete_student(self, student_id):
        student = request.env["dariora.student"].sudo().browse(student_id)

        if not student.exists():
            return cors_response(
                {"error": "Student not found"},
                status=404,
            )

        try:
            student.unlink()
            return cors_response(
                {"message": "Student deleted successfully"},
                status=200,
            )
        except Exception as e:
            return cors_response(
                {"error": str(e)},
                status=500,
            )

    # Enrollment API

    @http.route(
        "/api/enrollments",
        type="http",
        auth="user",
        methods=["GET"],
        csrf=False,
    )
    def get_enrollments(self):
        enrollments = request.env["dariora.enrollment"].sudo().search([])

        result = []

        for enrollment in enrollments:
            result.append({
                "id": enrollment.id,
                "student_id": enrollment.student_id.id,
                "student_name": enrollment.student_id.name,
                "course_id": enrollment.course_id.id,
                "course_name": enrollment.course_id.name,
                "enrollment_date": str(enrollment.enrollment_date),
                "status": enrollment.status,
            })

        return cors_response(result)

    @http.route(
        "/api/enrollments/<int:enrollment_id>",
        type="http",
        auth="user",
        methods=["GET"],
        csrf=False,
    )
    def get_enrollment(self, enrollment_id):
        enrollment = request.env["dariora.enrollment"].sudo().browse(
            enrollment_id
        )

        if not enrollment.exists():
            return cors_response(
                {"error": "Enrollment not found"},
                status=404,
            )

        return cors_response({
            "id": enrollment.id,
            "student_id": enrollment.student_id.id,
            "student_name": enrollment.student_id.name,
            "course_id": enrollment.course_id.id,
            "course_name": enrollment.course_id.name,
            "enrollment_date": str(enrollment.enrollment_date),
            "status": enrollment.status,
        })

    @http.route(
        "/api/enrollments",
        type="http",
        auth="user",
        methods=["POST"],
        csrf=False,
    )
    def create_enrollment(self):
        data = request.get_json_data()

        student_id = data.get("student_id")
        course_id = data.get("course_id")

        if not student_id:
            return cors_response(
                {"error": "student_id is required"},
                status=400,
            )

        if not course_id:
            return cors_response(
                {"error": "course_id is required"},
                status=400,
            )

        student = request.env["dariora.student"].sudo().browse(student_id)

        if not student.exists():
            return cors_response(
                {"error": "Student not found"},
                status=404,
            )

        course = request.env["dariora.course"].sudo().browse(course_id)

        if not course.exists():
            return cors_response(
                {"error": "Course not found"},
                status=404,
            )

        # Check for duplicate enrollment
        existing_enrollment = request.env["dariora.enrollment"].sudo().search([
            ("student_id", "=", student.id),
            ("course_id", "=", course.id),
        ])

        if existing_enrollment:
            return cors_response(
                {
                    "error": "Student is already enrolled in this course",
                    "enrollment_id": existing_enrollment[0].id,
                },
                status=409,
            )

        enrollment = request.env["dariora.enrollment"].sudo().create({
            "student_id": student.id,
            "course_id": course.id,
        })

        return cors_response(
            {
                "id": enrollment.id,
                "student_id": enrollment.student_id.id,
                "student_name": enrollment.student_id.name,
                "course_id": enrollment.course_id.id,
                "course_name": enrollment.course_id.name,
                "enrollment_date": str(enrollment.enrollment_date),
                "status": enrollment.status,
            },
            status=201,
        )

    @http.route(
        "/api/enrollments/<int:enrollment_id>",
        type="http",
        auth="user",
        methods=["PUT"],
        csrf=False,
    )
    def update_enrollment(self, enrollment_id):

        data = request.get_json_data()

        enrollment = request.env["dariora.enrollment"].sudo().browse(
            enrollment_id
        )

        if not enrollment.exists():
            return cors_response(
                {"error": "Enrollment not found"},
                status=404,
            )

        if "status" in data:
            if data["status"] not in ["active", "completed"]:
                return cors_response(
                    {
                        "error": "Status must be either active or completed"
                    },
                    status=400,
                )

            enrollment.write({
                "status": data["status"]
            })

        return cors_response({
            "id": enrollment.id,
            "student_id": enrollment.student_id.id,
            "student_name": enrollment.student_id.name,
            "course_id": enrollment.course_id.id,
            "course_name": enrollment.course_id.name,
            "enrollment_date": str(enrollment.enrollment_date),
            "status": enrollment.status,
        })

    @http.route(
        "/api/enrollments/<int:enrollment_id>",
        type="http",
        auth="user",
        methods=["DELETE"],
        csrf=False,
    )
    def delete_enrollment(self, enrollment_id):

        enrollment = request.env["dariora.enrollment"].sudo().browse(
            enrollment_id
        )

        if not enrollment.exists():
            return cors_response(
                {"error": "Enrollment not found"},
                status=404,
            )

        try:
            enrollment.unlink()
            return cors_response(
                {"message": "Enrollment deleted successfully"},
                status=200,
            )
        except Exception as e:
            return cors_response(
                {"error": str(e)},
                status=500,
            )

    # Authentication API

    @http.route(
        "/api/login",
        type="http",
        auth="none",
        methods=["POST"],
        csrf=False,
    )
    def login(self):

        data = request.get_json_data()

        login = data.get("login")

        if not login:
            return cors_response(
                {"error": "login is required"},
                status=400,
            )

        try:
            # For demo: allow login with any password (demo purposes)
            user = request.env['res.users'].sudo().search([('login', '=', login)], limit=1)
            
            if user:
                # Set the session properly using Odoo's method
                # For demo, we bypass password check
                request.session.uid = user.id
                
                return cors_response({
                    "message": "Login successful",
                    "user": {
                        "id": user.id,
                        "name": user.name,
                        "login": user.login,
                    },
                })
            else:
                return cors_response(
                    {"error": "User not found"},
                    status=401,
                )
        except Exception as e:
            return cors_response(
                {"error": f"Login failed: {str(e)}"},
                status=500,
            )

    @http.route(
        "/api/me",
        type="http",
        auth="user",
        methods=["GET"],
        csrf=False,
    )
    def get_current_user(self):

        user = request.env.user
        return cors_response({
            "id": user.id,
            "name": user.name,
            "login": user.login,
            "email": user.email,
        })

    @http.route(
        "/api/logout",
        type="http",
        auth="none",
        methods=["POST"],
        csrf=False,
    )
    def logout(self):

        if request.session.uid:
            request.session.logout()

        return cors_response({
            "message": "Logout successful"
        })

    @http.route(
        "/api/debug/users",
        type="http",
        auth="none",
        methods=["GET"],
        csrf=False,
    )
    def debug_users(self):
        """Debug endpoint to list all users"""
        users = request.env['res.users'].sudo().search([])
        result = []
        for user in users:
            result.append({
                "id": user.id,
                "name": user.name,
                "login": user.login,
            })
        return cors_response(result)
