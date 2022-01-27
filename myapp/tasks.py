from celery import shared_task
from time import sleep


@shared_task
def nlp_process(text):
    sleep(5)
    print("process")
    return "hello from nlp"


@shared_task
def test(a):
    return a ** 2
