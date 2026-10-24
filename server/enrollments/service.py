from enrollments.model import Enrollment
from enrollments.repository import EnrollmentRepository
from students.service import StudentService
from courses.service import CourseService

class EnrollmentService:
    def __init__(
        self,
        repository: EnrollmentRepository,
        student_service: StudentService,
        course_service: CourseService
    ):
        self.repository = repository
        self.student_service = student_service
        self.course_service = course_service

    def enroll(self, student_id: int, course_id: int) -> None:
        student = self.student_service.get_student(student_id)
        if student is None:
            raise ValueError(f"Student with ID {student_id} does not exist.")

        course = self.course_service.get_course(course_id)
        if course is None:
            raise ValueError(f"Course with ID {course_id} does not exist.")

        if self.repository.exists(student_id, course_id):
            raise ValueError("Student is already enrolled in this course.")

        enrollment = Enrollment(id=None, student_id=student_id, course_id=course_id)
        self.repository.add(enrollment)

    def get_enrollments(self) -> list[Enrollment]:
        return self.repository.get_all()