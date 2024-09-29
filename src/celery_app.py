import time
from celery import Celery

# Create a Celery instance using Redis as the broker
app = Celery(
    "celery_app",
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0"
)

# Celery configuration for task routing
app.conf.task_queues = {
    "high_priority_queue": {
        "exchange": "high_priority_exchange",
        "routing_key": "high_priority"
    },
    "low_priority_queue": {
        "exchange": "low_priority_exchange",
        "routing_key": "low_priority"
    }
}

app.conf.task_routes = {
    "celery_app.hight_priority_task": {"queue": "high_priority_queue", "routing_key": "hight_priority"},
    "celery_app.low_priority_task": {"queue": "low_priority_queue", "routing_key": "low_priority"}
}

app.conf.task_default_queue = "default_queue"
app.conf.task_default_exchange = "default"
app.conf.task_default_routing_key = "default"


@app.task(bind=True, max_retries=3)
def my_task(self):
    print("Hello Celery World!")


@app.task(bind=True, max_reties=10)
def countdown_test(self, greeting: str):
    print("Hey I'm count down..")
    print(greeting)


@app.task
def high_priority_task(task_id):
    print(f'High priority task {task_id} started.')
    time.sleep(5)
    print(f'High priority task {task_id} finished.')


@app.task
def low_priority_task(task_id):
    print(f'Low priority task {task_id} started.')
    time.sleep(5)
    print(f'Low priority task {task_id} finished.')


high_priority_task.apply_async((1,), queue="high_priority_queue")
low_priority_task.apply_async((2,), queue="low_priority_queue")
countdown_test.apply_async(("Hello World!",),countdown=10, queue="high_priority_queue")