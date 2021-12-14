from django.utils import timezone
from datetime import datetime


def convert_str_date_to_timezone_date(date):
    date = datetime.strptime(date, "%Y-%m-%d")
    return date.astimezone(timezone.get_current_timezone())
