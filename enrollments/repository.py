from database import get_connection
from enrollments.model import Enrollment

class EnrollmentRepository:
    def add(self, enrollment: Enrollment) -> None:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)",
            (enrollment.student_id, enrollment.course_id)
        )
        connection.commit()
        connection.close()

    def exists(self, student_id: int, course_id: int) -> bool:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT 1 FROM enrollments WHERE student_id = ? AND course_id = ?",
            (student_id, course_id)
        )
        row = cursor.fetchone()
        connection.close()
        return row is not None