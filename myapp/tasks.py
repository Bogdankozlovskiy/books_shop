from celery import shared_task


@shared_task(bind=True, name="myapp.tasks.add")
def add(self, x, y):
    print(self.retry)
    print("hello task")
    return x + y


# add.delay
# add.s
# add.apply_async