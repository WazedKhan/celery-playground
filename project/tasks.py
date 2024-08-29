from celery_app import celery_app
import time

@celery_app.task
def add_numbers(a: int, b: int) -> int:
    time.sleep(10)  # Simulate a long-running task
    return a + b
