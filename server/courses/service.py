from courses.model import Course
from courses.repository import CourseRepository


class CourseService:
    def __init__(self, repository: CourseRepository):
        self.repository = repository

    def create_course(self, name: str, teacher: str) -> Course:
        if not name.strip():
            raise ValueError("Course name is required")
        if not teacher.strip():
            raise ValueError("Teacher name is required")

        course = Course(id=None, name=name.strip(), teacher=teacher.strip())
        return self.repository.add(course)

    def get_courses(self) -> list[Course]:
        return self.repository.get_all()

    def get_course(self, course_id: int) -> Course | None:
        return self.repository.get_by_id(course_id)