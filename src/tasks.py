from celery_app import app

@app.task(bind=True, max_retries=3)
def my_task(self):
    print("Hello Celery World!")
