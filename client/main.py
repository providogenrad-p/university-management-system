from http_client import HTTPClient


def run_console(http_client):
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
                student = http_client.post(
                    "/students",
                    {
                        "name": name,
                        "email": email
                    }
                )
                print(f"Student created successfully (ID {student['id']}).")
            elif choice == "2":
                students = http_client.get("/students")
                print("\n--- Students ---")
                for student in students:
                    print(f"{student['id']}: {student['name']} ({student['email']})")
            elif choice == "3":
                name = input("Course name: ")
                teacher = input("Teacher name: ")
                course = http_client.post(
                    "/courses",
                    {
                        "name": name,
                        "teacher": teacher
                    }
                )
                print(f"Course created successfully (ID {course['id']}).")
            elif choice == "4":
                courses = http_client.get("/courses")
                print("\n--- Courses ---")
                for course in courses:
                    print(f"{course['id']}: {course['name']} - {course['teacher']}")
            elif choice == "5":
                student_id = int(input("Student ID: "))
                course_id = int(input("Course ID: "))
                http_client.post(
                    "/enrollments",
                    {
                        "student_id": student_id,
                        "course_id": course_id
                    }
                )
                print("Student enrolled successfully.")
            elif choice == "0":
                print("Application closed.")
                break
            else:
                print("Invalid option.")
        except ConnectionError as error:
            print(f"Error: {error}")
        except ValueError as error:
            print(f"Error: {error}")


def main():
    run_console(HTTPClient())


if __name__ == "__main__":
    main()