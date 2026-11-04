"""Filter: VALIDATE - remove records without a name or an e-mail."""


def has_value(value):
    return value is not None and value.strip() != ""


def process(students):
    valid_students = []
    for student in students:
        if not has_value(student.get("name")):
            continue
        if not has_value(student.get("email")):
            continue
        valid_students.append(student)
    return valid_students
