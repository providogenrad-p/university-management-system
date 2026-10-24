# University Management System

Console application in Python for managing students, courses and enrollments,
built step by step through three software architecture labs.

| Version | Lab | Architecture |
|---------|-----|--------------|
| `v1.0`  | Lab 1 | Modular Monolith |
| `v2.0`  | Lab 2 | Microkernel / Plug-in (report plug-ins) |
| `v3.0`  | Lab 3 | Client–Server, Multi-tier (HTTP + JSON) |

The current version (`main`) is **Lab 3**. Earlier versions are available under **Tags**.

Only the Python Standard Library is used – no Flask, FastAPI, Django or requests.

## Architecture

    PRESENTATION   Console Client  (client/)
          │
          │  HTTP + JSON
          ▼
    APPLICATION    Application Server → Services → Repositories  (server/)
          │
          ▼
    DATA           SQLite  (server/data/university.db)

The client and the server are separate programs.
The client never accesses the database directly – every operation goes through the HTTP API.
Several clients can use the same server at the same time and see the same data.

## How to run

Start the server and the client in **two separate terminals**, from the project folder:

    python server/application_server.py

    python client/main.py

The server must be started first. If it is not running, the client shows
`Error: Application Server is unavailable.`

To try multiple clients, start `python client/main.py` in a third terminal.

## API

| Method | Path           | Operation      | Request body                           |
|--------|----------------|----------------|----------------------------------------|
| GET    | `/students`    | List students  | –                                      |
| POST   | `/students`    | Create student | `{"name": "...", "email": "..."}`      |
| GET    | `/courses`     | List courses   | –                                      |
| POST   | `/courses`     | Create course  | `{"name": "...", "teacher": "..."}`    |
| POST   | `/enrollments` | Enroll student | `{"student_id": 1, "course_id": 1}`    |

Status codes: `200 OK`, `201 Created`, `400 Bad Request`, `404 Not Found`, `500 Internal Server Error`.

The GET endpoints can also be opened in a browser:
http://127.0.0.1:8080/students and http://127.0.0.1:8080/courses

## Project structure

    client/
      main.py                 console menu
      http_client.py          sends HTTP requests over socket
    server/
      application_server.py   HTTP server: parses requests, calls services, sends JSON
      database.py             SQLite connection and tables
      students/               model, repository, service
      courses/                model, repository, service
      enrollments/            model, repository, service
      data/university.db      database (created automatically)

## Business rules

The rules stay in the services on the server:
- student name is required and the email must be valid;
- course name and teacher are required;
- a student can be enrolled only in an existing course, and only once.