from celery import shared_task
from time import sleep


@shared_task
def nlp_process(text):
    sleep(5)
    print("process")
