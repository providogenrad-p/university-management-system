from database import get_connection
from courses.model import Course

class CourseRepository:
    def add(self, course: Course) -> None:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO courses (name, teacher) VALUES (?, ?)",
            (course.name, course.teacher)
        )
        connection.commit()
        connection.close()

    def get_all(self) -> list[Course]:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, teacher FROM courses")
        rows = cursor.fetchall()
        connection.close()
        return [Course(id=row[0], name=row[1], teacher=row[2]) for row in rows]

    def get_by_id(self, course_id: int) -> Course | None:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, teacher FROM courses WHERE id = ?", (course_id,))
        row = cursor.fetchone()
        connection.close()
        if row:
            return Course(id=row[0], name=row[1], teacher=row[2])
        return None