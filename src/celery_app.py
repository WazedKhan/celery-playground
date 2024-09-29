from celery import Celery

# Create a Celery instance using Redis as the broker
app = Celery("celery_app", broker="redis://127.0.0.1:6379/0")



@app.task(bind=True, max_retries=3)
def my_task(self):
    print("Hello Celery World!")


@app.task(bind=True, max_reties=10)
def countdown_test(self, greeting: str):
    print("Hey I'm count down..")
    print(greeting)
