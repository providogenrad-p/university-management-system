from database import get_connection
from students.model import Student

class StudentRepository:
    def add(self, student: Student) -> None:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO students (name, email) VALUES (?, ?)",
            (student.name, student.email)
        )
        connection.commit()
        connection.close()

    def get_all(self) -> list[Student]:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, email FROM students")
        rows = cursor.fetchall()
        connection.close()
        return [Student(id=row[0], name=row[1], email=row[2]) for row in rows]

    def get_by_id(self, student_id: int) -> Student | None:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, email FROM students WHERE id = ?", (student_id,))
        row = cursor.fetchone()
        connection.close()
        if row:
            return Student(id=row[0], name=row[1], email=row[2])
        return None