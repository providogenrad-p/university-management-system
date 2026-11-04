"""Starts the student import. Not a filter - it only prepares and runs the pipeline.

Run from the project folder:
    python server/import_students.py
    python server/import_students.py server/import_data/order_test.csv
"""
import os
import sys

from database import initialize_database
from students.repository import StudentRepository
from students.service import StudentService
from import_pipeline import pipeline

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_FILE = os.path.join(BASE_DIR, "import_data", "students.csv")


def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILE

    if not os.path.isfile(filename):
        print(f"File not found: {filename}")
        return

    initialize_database()
    student_service = StudentService(StudentRepository())

    print(f"Importing {filename}\n")
    stored = pipeline.run(filename, student_service)

    print(f"\nImported students: {len(stored)}")
    for student in stored:
        print(f"  {student['name']} <{student['email']}>")


if __name__ == "__main__":
    main()
