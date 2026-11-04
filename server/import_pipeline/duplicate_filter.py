"""Filter: CHECK DUPLICATES - keep only the first record for each e-mail."""


def process(students):
    result = []
    seen = set()
    for student in students:
        email = student["email"]
        if email in seen:
            continue
        seen.add(email)
        result.append(student)
    return result
