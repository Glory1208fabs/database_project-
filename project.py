from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# Database connection setup
try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456789',
        database='task_manager'
    )
    print("Connected successfully!")
except mysql.connector.Error as err:
    print("Error:", err)

# Pydantic models for request/response schemas
class Task(BaseModel):
    id: int = None
    title: str
    description: str = None
    user_id: int
    category_id: int
    status: str = 'Pending'

@app.post("/tasks/")
def create_task(task: Task):
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description, user_id, category_id, status) VALUES (%s, %s, %s, %s, %s)",
        (task.title, task.description, task.user_id, task.category_id, task.status)
    )
    connection.commit()
    task.id = cursor.lastrowid
    return task

@app.get("/tasks/{task_id}")
def read_task(task_id: int):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE tasks SET title=%s, description=%s, user_id=%s, category_id=%s, status=%s WHERE id=%s",
        (task.title, task.description, task.user_id, task.category_id, task.status, task_id)
    )
    connection.commit()
    return {"message": "Task updated successfully"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    connection.commit()
    return {"message": "Task deleted successfully"}
