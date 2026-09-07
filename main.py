
from fastapi import FastAPI, HTTPException
import sqlite3
from pydantic import BaseModel

class Task(BaseModel):
    id: int
    task: str
    done: str

def get_db_connection():
    conn = sqlite3.connect("/app/data/crud_api.db")
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

api = FastAPI()

@api.get("/")
def greet():
    return {"message": "Welcome to the CRUD api with db"}

@api.get("/fetch_tasks")
def fetch_tasks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks;")
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@api.get("/fetch_tasks/{id}")
def fetch_tasks_by_id(id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE id = ?;", (id,))
    row = cur.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    raise HTTPException(status_code=404, detail="Task not found.")

@api.post("/add_task")
def add_task(task: Task):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tasks (id, task, done) VALUES (?, ?, ?);",
            (task.id, task.task, task.done)
        )
        conn.commit()
        conn.close()
        return {"message": f"Task Added with id: {task.id}"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Task ID already exists.")

@api.put("/update_task/{id}")
def update_task(id: int, task: Task):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE tasks SET id = ?, task = ?, done = ? WHERE id = ?;",
        (task.id, task.task, task.done, id)
    )
    conn.commit()
    changes = conn.total_changes
    conn.close()
    
    if changes == 0:
        raise HTTPException(status_code=404, detail="Task not found to update.")
    return {"message": "Task Updated successfully"}

@api.delete("/delete_task/{id}")
def delete_task(id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = ?;", (id,))
    conn.commit()
    
    changes = conn.total_changes
    conn.close()
    
    if changes == 0:
        raise HTTPException(status_code=404, detail="Task not found to delete.")
    return {"message": "Item Deleted successfully."}
