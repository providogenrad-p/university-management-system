from dataclasses import dataclass

@dataclass
class Enrollment:
    id: int | None
    student_id: int
    course_id: int