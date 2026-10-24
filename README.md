# University Management System

Console application in Python for managing students, courses and enrollments.

Only the Python Standard Library is used.

## Run

    python main.py

## Menu

    1. Add Student
    2. List Students
    3. Add Course
    4. List Courses
    5. Enroll Student in Course
    6. Generate Report
    0. Exit

## Project structure

    main.py              console menu (core)
    database.py          SQLite connection
    students/            model, repository, service
    courses/             model, repository, service
    enrollments/         model, repository, service
    plugin_manager.py    discovers, loads and validates plug-ins
    plugins/             report plug-ins
      txt_report.py        -> reports/students.txt
      statistics_report.py -> reports/statistics.txt
    data/university.db   database (created automatically)
    reports/             generated reports (created automatically)

## Plug-ins

Every plug-in in `plugins/` must provide two functions:

    def get_name():        # name shown in the menu
    def generate(data):    # creates the report, returns the file path

`data` is a dictionary prepared by the core:

    {"students": [...], "courses": [...], "enrollments": [...]}

The Plug-in Manager finds the plug-ins automatically with `os.listdir` and loads them with `importlib`.
Files that don't follow the contract are skipped and the application keeps running.

### Adding a new report

Create a new file in `plugins/` (for example `html_report.py`) with `get_name()` and `generate(data)`,
then restart the application. The new report appears in menu option 6 – no changes to the core are needed.