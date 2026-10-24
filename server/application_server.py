import json
import socket

from database import initialize_database
from students.repository import StudentRepository
from students.service import StudentService
from courses.repository import CourseRepository
from courses.service import CourseService
from enrollments.repository import EnrollmentRepository
from enrollments.service import EnrollmentService

HOST = "127.0.0.1"
PORT = 8080

initialize_database()

student_service = StudentService(StudentRepository())
course_service = CourseService(CourseRepository())
enrollment_service = EnrollmentService(
    EnrollmentRepository(),
    student_service,
    course_service
)

STATUS_TEXT = {
    200: "OK",
    201: "Created",
    400: "Bad Request",
    404: "Not Found",
    500: "Internal Server Error"
}


# ---------- Task 2: read the complete HTTP request ----------

def receive_request(client):
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = client.recv(4096)
        if not chunk:
            break
        data += chunk

    header_bytes, _, body_bytes = data.partition(b"\r\n\r\n")
    headers = header_bytes.decode("utf-8")

    content_length = 0
    for line in headers.split("\r\n")[1:]:
        name, _, value = line.partition(":")
        if name.strip().lower() == "content-length":
            content_length = int(value.strip())

    while len(body_bytes) < content_length:
        chunk = client.recv(4096)
        if not chunk:
            break
        body_bytes += chunk

    return headers, body_bytes.decode("utf-8")


# ---------- Task 3: send an HTTP response ----------

def send_response(client, status, data):
    body = json.dumps(data, ensure_ascii=False)
    body_bytes = body.encode("utf-8")
    headers = (
        f"HTTP/1.1 {status} {STATUS_TEXT[status]}\r\n"
        "Content-Type: application/json; charset=utf-8\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    client.sendall(headers.encode("utf-8") + body_bytes)


# ---------- Objects -> dictionaries (JSON) ----------

def student_to_dict(student):
    return {
        "id": student.id,
        "name": student.name,
        "email": student.email
    }


def course_to_dict(course):
    return {
        "id": course.id,
        "name": course.name,
        "teacher": course.teacher
    }


def enrollment_to_dict(enrollment):
    return {
        "id": enrollment.id,
        "student_id": enrollment.student_id,
        "course_id": enrollment.course_id
    }


# ---------- Tasks 3-5: routing ----------

def handle_request(method, path, body):
    path = path.split("?")[0]  # ignore query string, e.g. /students?x=1

    # Students
    if method == "GET" and path == "/students":
        students = student_service.get_students()
        return 200, [student_to_dict(s) for s in students]

    if method == "POST" and path == "/students":
        data = json.loads(body)
        student = student_service.create_student(
            data["name"],
            data["email"]
        )
        return 201, student_to_dict(student)

    # Courses
    if method == "GET" and path == "/courses":
        courses = course_service.get_courses()
        return 200, [course_to_dict(c) for c in courses]

    if method == "POST" and path == "/courses":
        data = json.loads(body)
        course = course_service.create_course(
            data["name"],
            data["teacher"]
        )
        return 201, course_to_dict(course)

    # Enrollments
    if method == "POST" and path == "/enrollments":
        data = json.loads(body)
        enrollment = enrollment_service.enroll(
            int(data["student_id"]),
            int(data["course_id"])
        )
        return 201, enrollment_to_dict(enrollment)

    return 404, {"error": f"Unknown endpoint: {method} {path}"}


# ---------- Server loop ----------

def main():
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server running on http://{HOST}:{PORT}")

    while True:
        client, address = server.accept()
        try:
            headers, body = receive_request(client)
            if not headers:
                continue

            method, path, version = headers.split("\r\n")[0].split()
            print(method, path)

            try:
                status, data = handle_request(method, path, body)
            except KeyError as error:
                status, data = 400, {"error": f"Missing field: {error}"}
            except ValueError as error:
                status, data = 400, {"error": str(error)}
            except Exception as error:
                print(f"Internal error: {error!r}")
                status, data = 500, {"error": "Internal server error"}

            send_response(client, status, data)
        except Exception as error:
            print(f"Could not process request: {error!r}")
        finally:
            client.close()


if __name__ == "__main__":
    main()