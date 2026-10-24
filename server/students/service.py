from students.model import Student
from students.repository import StudentRepository


class StudentService:
    def __init__(self, repository: StudentRepository):
        self.repository = repository

    def create_student(self, name: str, email: str) -> None:
        if not name.strip():
            raise ValueError("Student name is required")
        if "@" not in email:
            raise ValueError("Invalid email format")

        student = Student(id=None, name=name.strip(), email=email.strip())
        self.repository.add(student)

    def get_students(self) -> list[Student]:
        return self.repository.get_all()

    def get_student(self, student_id: int) -> Student | None:
        return self.repository.get_by_id(student_id)