"""Filter: NORMALIZE - clean up names and e-mails."""


def process(students):
    result = []
    for student in students:
        normalized = student.copy()
        # " Ivan   Petrov " -> "Ivan Petrov"
        normalized["name"] = " ".join(student["name"].split())
        # " IVAN@TU-SOFIA.BG " -> "ivan@tu-sofia.bg"
        normalized["email"] = student["email"].strip().lower()
        result.append(normalized)
    return result
