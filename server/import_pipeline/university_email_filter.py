"""Filter: UNIVERSITY EMAIL - keep only @tu-sofia.bg addresses.

Must run after NORMALIZE: before that, "IVAN.PETROV@TU-SOFIA.BG"
does not end with "@tu-sofia.bg".
"""

UNIVERSITY_DOMAIN = "@tu-sofia.bg"


def process(students):
    result = []
    for student in students:
        if student["email"].endswith(UNIVERSITY_DOMAIN):
            result.append(student)
    return result
