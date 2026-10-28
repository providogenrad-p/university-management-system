"""Fill the database with sample data.

Run from the project folder:
    python server/seed_data.py

The data goes through the services, so all business rules
(valid email, existing student/course, no duplicate enrollment)
are applied exactly as for data entered from the client.
Running the script again does not create duplicates.
"""
import random

from database import initialize_database
from students.repository import StudentRepository
from students.service import StudentService
from courses.repository import CourseRepository
from courses.service import CourseService
from enrollments.repository import EnrollmentRepository
from enrollments.service import EnrollmentService

STUDENTS = [
    ("Maria Ivanova", "maria.ivanova@university.bg"),
    ("Ivan Petrov", "ivan.petrov@university.bg"),
    ("Georgi Dimitrov", "georgi.dimitrov@university.bg"),
    ("Elena Georgieva", "elena.georgieva@university.bg"),
    ("Nikolay Stoyanov", "nikolay.stoyanov@university.bg"),
    ("Desislava Todorova", "desislava.todorova@university.bg"),
    ("Petar Nikolov", "petar.nikolov@university.bg"),
    ("Viktoria Hristova", "viktoria.hristova@university.bg"),
    ("Aleksandar Kolev", "aleksandar.kolev@university.bg"),
    ("Yana Pavlova", "yana.pavlova@university.bg"),
    ("Dimitar Angelov", "dimitar.angelov@university.bg"),
    ("Kristina Marinova", "kristina.marinova@university.bg"),
    ("Stefan Iliev", "stefan.iliev@university.bg"),
    ("Gabriela Petkova", "gabriela.petkova@university.bg"),
    ("Martin Vasilev", "martin.vasilev@university.bg"),
    ("Simona Atanasova", "simona.atanasova@university.bg"),
    ("Hristo Yordanov", "hristo.yordanov@university.bg"),
    ("Radostina Koleva", "radostina.koleva@university.bg"),
    ("Todor Mihaylov", "todor.mihaylov@university.bg"),
    ("Iva Dimitrova", "iva.dimitrova@university.bg"),
    ("Boris Kostadinov", "boris.kostadinov@university.bg"),
    ("Teodora Ivanova", "teodora.ivanova@university.bg"),
    ("Kaloyan Stefanov", "kaloyan.stefanov@university.bg"),
    ("Mihaela Popova", "mihaela.popova@university.bg"),
    ("Ventsislav Genchev", "ventsislav.genchev@university.bg"),
    ("Nadezhda Ruseva", "nadezhda.ruseva@university.bg"),
    ("Lyubomir Zhelev", "lyubomir.zhelev@university.bg"),
    ("Polina Stancheva", "polina.stancheva@university.bg"),
    ("Emil Tsvetkov", "emil.tsvetkov@university.bg"),
    ("Silvia Nedelcheva", "silvia.nedelcheva@university.bg"),
]

COURSES = [
    ("Software Architecture", "Prof. Ivan Georgiev"),
    ("Databases", "Assoc. Prof. Maria Petrova"),
    ("Object-Oriented Programming", "Prof. Ivan Georgiev"),
    ("Computer Networks", "Dr. Nikolay Dimov"),
    ("Web Technologies", "Dr. Elena Vasileva"),
    ("Operating Systems", "Assoc. Prof. Stoyan Marinov"),
    ("Algorithms and Data Structures", "Prof. Petya Koleva"),
    ("Information Security", "Dr. Nikolay Dimov"),
]

ENROLLMENTS_PER_STUDENT = (2, 4)  # every student gets between 2 and 4 courses


def main():
    initialize_database()

    student_service = StudentService(StudentRepository())
    course_service = CourseService(CourseRepository())
    enrollment_service = EnrollmentService(
        EnrollmentRepository(),
        student_service,
        course_service
    )

    # Students - skip the ones that already exist (email is unique)
    existing_emails = {s.email for s in student_service.get_students()}
    added_students = 0
    for name, email in STUDENTS:
        if email not in existing_emails:
            student_service.create_student(name, email)
            added_students += 1

    # Courses - skip the ones that already exist (same name)
    existing_courses = {c.name for c in course_service.get_courses()}
    added_courses = 0
    for name, teacher in COURSES:
        if name not in existing_courses:
            course_service.create_course(name, teacher)
            added_courses += 1

    # Enrollments - random, but the same every time (fixed seed)
    rng = random.Random(42)
    students = student_service.get_students()
    courses = course_service.get_courses()
    added_enrollments = 0
    for student in students:
        count = min(rng.randint(*ENROLLMENTS_PER_STUDENT), len(courses))
        for course in rng.sample(courses, count):
            try:
                enrollment_service.enroll(student.id, course.id)
                added_enrollments += 1
            except ValueError:
                pass  # already enrolled - business rule in EnrollmentService

    print("Sample data loaded:")
    print(f"  students:    +{added_students} (total {len(students)})")
    print(f"  courses:     +{added_courses} (total {len(courses)})")
    print(f"  enrollments: +{added_enrollments}")


if __name__ == "__main__":
    main()
