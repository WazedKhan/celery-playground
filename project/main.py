from fastapi import FastAPI, BackgroundTasks
from celery.result import AsyncResult
from tasks import add_numbers

app = FastAPI()

@app.post("/add/")
async def add(a: int, b: int, background_tasks: BackgroundTasks):
    task = add_numbers.delay(a, b)
    return {"task_id": task.id}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    task_result = AsyncResult(task_id)
    if task_result.state == "SUCCESS":
        return {"status": "Task completed", "result": task_result.result}
    elif task_result.state == "FAILURE":
        return {"status": "Task failed", "result": str(task_result.result)}
    else:
        return {"status": task_result.state}
