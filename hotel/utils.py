from django.utils import timezone
from datetime import datetime


def convert_str_date_to_timezone_date(date):
    date = datetime.strptime(date, "%Y-%m-%d")
    return date.astimezone(timezone.get_current_timezone())


class MyCustomFilter:
    def filter_queryset(self, request, queryset, view):
        for key, value in request.query_params.items():
            if key in view.filtering_fields:
                queryset = queryset.filter(**{key: value})
        return queryset

