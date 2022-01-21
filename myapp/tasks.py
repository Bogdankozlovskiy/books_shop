from celery import shared_task


@shared_task(bind=True)
def add(self, x, y):
    print(self.retry)
    print("hello task")
    return x + y
