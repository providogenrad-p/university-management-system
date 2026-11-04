# University Management System

Console application in Python for managing students, courses and enrollments,
built step by step through four software architecture labs.

| Version | Lab | Architecture |
|---------|-----|--------------|
| `v1.0`  | Lab 1 | Modular Monolith |
| `v2.0`  | Lab 2 | Microkernel / Plug-in (report plug-ins) |
| `v3.0`  | Lab 3 | Client–Server, Multi-tier (HTTP + JSON) |
| `v4.0`  | Lab 4 | Pipes & Filters (CSV student import) |

The current version (`main`) is **Lab 4**. Earlier versions are available under **Tags**.

Only the Python Standard Library is used – no Flask, FastAPI, Django or requests.

## Architecture

    PRESENTATION   Console Client  (client/)
          │
          │  HTTP + JSON
          ▼
    APPLICATION    Application Server → Services → Repositories  (server/)
          │                                ▲
          ▼                                │
    DATA           SQLite  ◄──── Student Import (Pipes & Filters, server-side batch)

- The client never accesses the database directly – every operation goes through the HTTP API.
- The CSV import runs on the server side and stores students through the same `StudentService`,
  so the same business rules apply and imported students are visible to every client.

## How to run

From the project folder, in **two separate terminals**:

    python server/application_server.py

    python client/main.py

The server must be started first. The GET endpoints can also be opened in a browser:
http://127.0.0.1:8080/students and http://127.0.0.1:8080/courses

### Import students from CSV

    python server/import_students.py
    python server/import_students.py path/to/file.csv

The default file is `server/import_data/students.csv`. The console shows how many records
remain after each filter and which records were rejected.

### Sample data (optional)

    python server/seed_data.py

Loads 30 students, 8 courses and their enrollments for demonstration.

## Import pipeline (Lab 4)

    students.csv
        → READ               read the CSV into a list of dictionaries
        → VALIDATE           remove records without name or e-mail
        →