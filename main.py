from database import initialize_database
from students.repository import StudentRepository
from students.service import StudentService
from courses.repository import CourseRepository
from courses.service import CourseService
from enrollments.repository import EnrollmentRepository
from enrollments.service import EnrollmentService

def run_console(student_service, course_service, enrollment_service):
    while True:
        print("\n=== University Management System ===")
        print("1. Add Student")
        print("2. List Students")
        print("3. Add Course")
        print("4. List Courses")
        print("5. Enroll Student in Course")
        print("0. Exit")
        choice = input("\nSelect option: ")

        try:
            if choice == "1":
                name = input("Student name: ")
                email = input("Student email: ")
                student_service.create_student(name, email)
                print("Student created successfully.")
            elif choice == "2":
                students = student_service.get_students()
                print("\n--- Students ---")
                for student in students:
                    print(f"{student.id}: {student.name} ({student.email})")
            elif choice == "3":
                name = input("Course name: ")
                teacher = input("Teacher name: ")
                course_service.create_course(name, teacher)
                print("Course created successfully.")
            elif choice == "4":
                courses = course_service.get_courses()
                print("\n--- Courses ---")
                for course in courses:
                    print(f"{course.id}: {course.name} - {course.teacher}")
            elif choice == "5":
                student_id = int(input("Student ID: "))
                course_id = int(input("Course ID: "))
                enrollment_service.enroll(student_id, course_id)
                print("Student enrolled successfully.")
            elif choice == "0":
                print("Application closed.")
                break
            else:
                print("Invalid option.")
        except ValueError as error:
            print(f"Error: {error}")
        except Exception as e:
            print(f"Unexpected error: {e}")

def main():
    initialize_database()

    student_repository = StudentRepository()
    student_service = StudentService(student_repository)

    course_repository = CourseRepository()
    course_service = CourseService(course_repository)

    enrollment_repository = EnrollmentRepository()
    enrollment_service = EnrollmentService(
        enrollment_repository,
        student_service,
        course_service
    )

    run_console(student_service, course_service, enrollment_service)

if __name__ == "__main__":
    main()