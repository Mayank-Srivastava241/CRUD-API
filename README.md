# CRUD API

A simple CRUD API built with **FastAPI**, developed progressively across three versions to demonstrate the evolution from in-memory data storage to persistent database storage and finally containerization.

## Project Evolution

| Version  | Focus                   | Implementation                                                       |
| -------- | ----------------------- | -------------------------------------------------------------------- |
| **v1.0** | In-Memory CRUD          | Tasks stored directly in Python memory                               |
| **v2.0** | Database Implementation | SQLite database used for persistent storage                          |
| **v3.0** | Containerization        | FastAPI application containerized with Docker and SQLite persistence |

---

# v1.0 — In-Memory Implementation

The first version implements a basic CRUD API using an in-memory Python list.

### Architecture

```text
Client
  │
  ▼
FastAPI
  │
  ▼
Python List
```

The tasks exist only while the application is running.

### Operations

* Create a task
* Read all tasks
* Read a task by ID
* Update a task
* Delete a task

### Limitation

Because the data is stored in application memory, restarting the FastAPI application removes all tasks.

This version was primarily focused on understanding:

* FastAPI
* HTTP methods
* CRUD operations
* Request/response handling
* Pydantic models
* API routing

---

# v2.0 — Database Implementation

The second version replaces the in-memory task list with a **SQLite database**.

The API uses Python's built-in `sqlite3` module to connect to the database and execute SQL queries.

### Architecture

```text
Client
  │
  ▼
FastAPI
  │
  ▼
SQLite Database
```

The database stores the tasks instead of keeping them only in application memory.

### Database Model

The `tasks` table contains:

| Column | Type    | Description            |
| ------ | ------- | ---------------------- |
| `id`   | INTEGER | Unique task identifier |
| `task` | TEXT    | Task description       |
| `done` | TEXT    | Task completion status |

### CRUD Operations

The API provides:

```text
GET    /fetch_tasks
GET    /fetch_tasks/{id}
POST   /add_task
PUT    /update_task/{id}
DELETE /delete_task/{id}
```

The implementation performs SQL operations such as:

```sql
SELECT
INSERT
UPDATE
DELETE
```

The database connection is created through a dedicated connection function, while the individual API endpoints execute the required SQL queries.

### Improvement over v1.0

Unlike the in-memory implementation, data can survive application restarts because it is stored in a SQLite database file.

### Limitation

At this stage, the application depends directly on SQLite and the database file location. The application also runs directly on the host machine rather than inside a reproducible containerized environment.

---

# v3.0 — Containerization

The third version containerizes the FastAPI application using **Docker**.

The goal is to make the application easier to run consistently while maintaining persistent SQLite storage.

### Architecture

```text
                 Docker
┌──────────────────────────────────────┐
│                                      │
│  FastAPI Application                 │
│       │                              │
│       ▼                              │
│  /app/data/crud_api.db               │
│       │                              │
└───────┼──────────────────────────────┘
        │
        │ Bind Mount
        ▼
Host Machine
/media/mayank/1978B452413EEDBB/
    sqlite_db/
        crud_api.db
```

The SQLite database is stored on the host machine and mounted into the container.

### Docker Compose

The complete application can be started using:

```bash
docker compose up --build
```

This removes the need to manually start the FastAPI server.

### Persistence

The database directory is mounted into the container:

```yaml
volumes:
  - /media/mayank/1978B452413EEDBB/sqlite_db:/app/data
```

Inside the container, the application accesses:

```text
/app/data/crud_api.db
```

which corresponds to the database file on the host.

Therefore, removing and recreating the application container does not remove the SQLite database.

### Persistence Test

Persistence can be demonstrated using the following process:

```text
1. Start the application
        ↓
2. Add a task
        ↓
3. Verify the task exists
        ↓
4. Stop the container
        ↓
5. Start the container again
        ↓
6. Fetch the tasks
        ↓
7. Previously created task still exists
```

The database remains on the host through the bind mount, allowing the application to access the same data after container recreation.

---

# Running the Project

## Prerequisites

* Docker
* Docker Compose

For v1.0 and v2.0, Python and the required Python packages are also needed if running the application directly.

---

## Running v3.0

Clone the repository and enter the project directory:

```bash
git clone https://github.com/Mayank-Srivastava241/CRUD-API.git
cd CRUD-API
```

Start the application:

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

FastAPI's interactive API documentation is available at:

```text
http://localhost:8000/docs
```

---

# API Endpoints

| Method | Endpoint            | Purpose                 |
| ------ | ------------------- | ----------------------- |
| GET    | `/`                 | API welcome message     |
| GET    | `/fetch_tasks`      | Fetch all tasks         |
| GET    | `/fetch_tasks/{id}` | Fetch a task by ID      |
| POST   | `/add_task`         | Add a new task          |
| PUT    | `/update_task/{id}` | Update an existing task |
| DELETE | `/delete_task/{id}` | Delete a task           |

---

# Example Request

### Add a Task

```json
{
    "id": 1,
    "task": "Learn Docker",
    "done": "false"
}
```

### Example Response

```json
{
    "message": "Task Added with id: 1"
}
```

---

# Version History

## v1.0 — In-Memory CRUD

Initial implementation of the CRUD API.

**Main concept:** CRUD operations using an in-memory Python data structure.

---

## v2.0 — SQLite Database

Replaced in-memory storage with SQLite.

**Main concept:** Persistent data storage using a relational database.

---

## v3.0 — Docker Containerization

Containerized the FastAPI application and configured persistent SQLite storage through a host bind mount.

**Main concept:** Reproducible application deployment and persistent container storage.

---

# Learning Progression

The project demonstrates a gradual evolution of the same CRUD application:

```text
v1.0
In-Memory Storage
      │
      ▼
v2.0
SQLite Persistence
      │
      ▼
v3.0
Docker + Persistent Storage
```

Each version builds on the previous one rather than replacing the entire application.

The progression demonstrates three important concepts:

1. **API development** — building CRUD endpoints with FastAPI.
2. **Data persistence** — moving from temporary in-memory data to SQLite.
3. **Containerization** — packaging the application with Docker while keeping database data persistent.
