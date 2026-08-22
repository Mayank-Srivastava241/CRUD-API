from fastapi import FastAPI
from .model import Task
api = FastAPI()

tasks:list[Task] = [
    {
        "id": 2,
        "task": "Want to be the very best",
        "due": "2026-08-22T10:00:49.735Z"
    },
    {
        "id": 3,
        "task": "Like no one ever was",
        "due": "2026-08-23T12:00:00.000Z"
    },
    {
        "id": 4,
        "task": "To catch them is my real test",
        "due": "2026-08-24T15:30:00.000Z"
    }

]

@api.get("/")
def greet():
    return "Welcome to My CRUD API server"

@api.get('/fetch_task')
def fetch_task():
    if tasks:
        return tasks
    return "No tasks Pending"

@api.get("/fetch_task/{id}")
def fetch_by_id( id : int):
    for task in tasks:
        if task["id"] == id:
            return task
    return "No task Found"

@api.post("/add_task")
def add_task(task:list[Task]):
    if task:
        tasks.append(task)
        return task
    return "enter a proper task"

@api.put("/update_task/{id}")
def update_task(id :int,task:Task):
    for i in range(len(tasks)):
        if tasks[i]["id"] == id:
            tasks[i] = task
            return "Item Updated"
    return "No item found to be updated"

@api.delete("/delete_task/{id}")
def delete_task(id:int):
    for i in range(len(tasks)):
        if(tasks[i]["id"] == id):
            del tasks[i]
            return f"Item id:{id} deleted"
    return "Item not found"
