"""Filter: TRANSFORM - keep only the fields the system stores."""

FIELDS = ("name", "email")


def process(students):
    result = []
    for student in students:
        transformed = {field: student[field] for field in FIELDS}
        result.append(transformed)
    return result
