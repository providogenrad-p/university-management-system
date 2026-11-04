"""Filter: STORE - save students through StudentService (no SQL here)."""


def process(students, student_service):
    stored = []
    for student in students:
        try:
            student_service.create_student(
                student["name"],
                student["email"]
            )
            stored.append(student)
        except ValueError as error:
            print(f"  Rejected: {student['email']} - {error}")
    return stored
