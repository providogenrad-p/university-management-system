import os

REPORTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "reports"
)


def get_name():
    return "Statistics Report"


def generate(data):
    os.makedirs(REPORTS_DIR, exist_ok=True)
    filename = os.path.join(REPORTS_DIR, "statistics.txt")

    students = data["students"]
    courses = data["courses"]
    # Optional key - the plug-in still works if the core does not send it.
    enrollments = data.get("enrollments", [])
    teachers = sorted({course.teacher for course in courses})

    with open(filename, "w", encoding="utf-8") as file:
        file.write("UNIVERSITY STATISTICS\n\n")
        file.write(f"Total students: {len(students)}\n")
        file.write(f"Total courses: {len(courses)}\n")
        file.write(f"Total teachers: {len(teachers)}\n")
        file.write(f"Total enrollments: {len(enrollments)}\n")

        if teachers:
            file.write("\nCourses per teacher:\n")
            for teacher in teachers:
                count = sum(1 for course in courses if course.teacher == teacher)
                file.write(f"  {teacher}: {count}\n")

        if courses and enrollments:
            file.write("\nStudents per course:\n")
            for course in courses:
                count = sum(1 for e in enrollments if e.course_id == course.id)
                file.write(f"  {course.name}: {count}\n")

    return filename
