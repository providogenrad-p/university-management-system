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

    def get_all(self) -> list[Enrollment]:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, student_id, course_id FROM enrollments")
        rows = cursor.fetchall()
        connection.close()
        return [Enrollment(id=row[0], student_id=row[1], course_id=row[2]) for row in rows]