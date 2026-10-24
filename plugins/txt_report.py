import os

REPORTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "reports"
)


def get_name():
    return "TXT Report"


def generate(data):
    os.makedirs(REPORTS_DIR, exist_ok=True)
    filename = os.path.join(REPORTS_DIR, "students.txt")
    students = data["students"]

    with open(filename, "w", encoding="utf-8") as file:
        file.write("UNIVERSITY STUDENTS REPORT\n\n")
        if not students:
            file.write("No students registered.\n")
        for number, student in enumerate(students, start=1):
            file.write(f"{number}. {student.name}\n")
            file.write(f"   {student.email}\n\n")

    return filename
