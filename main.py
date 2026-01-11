from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from models import Task
from database import get_session, create_db_and_tables

app = FastAPI(title="Task API with SQLModel + Neon")


# 🔹 Create tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# 🔹 CREATE TASK
@app.post("/tasks", status_code=201)
def create_task(task: Task, session: Session = Depends(get_session)):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


# 🔹 READ ALL TASKS
@app.get("/tasks")
def get_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    return tasks


# 🔹 READ SINGLE TASK
@app.get("/-tasks/{task_id}")
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# 🔹 UPDATE TASK
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: Task, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = task_update.title
    task.description = task_update.description
    task.status = task_update.status

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


# 🔹 DELETE TASK
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return None
