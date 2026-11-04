"""Filter: READ - CSV file -> list of dictionaries."""
import csv


def process(filename):
    students = []
    # utf-8-sig also reads files saved by Excel as "CSV UTF-8" (with BOM)
    with open(filename, newline="", encoding="utf-8-sig") as file:
        # Excel with Bulgarian regional settings separates columns with ";"
        first_line = file.readline()
        delimiter = ";" if first_line.count(";") > first_line.count(",") else ","
        file.seek(0)

        reader = csv.DictReader(file, delimiter=delimiter)
        for row in reader:
            students.append(row)
    return students
