from abc import ABC
from django.contrib import admin

import pytz
from django.utils import timezone

def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter, ABC):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper

# Capitalize




def convert_to_localtime(utctime):
    fmt = '%Y-%m-%d %I:%M %p'
    utc = utctime.replace(tzinfo=pytz.UTC)
    localtz = utc.astimezone(timezone.get_current_timezone())

    return localtz.strftime(fmt)