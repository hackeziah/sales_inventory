from django.urls import path

from account.views import (
    register, users
)

urlpatterns = [
    path('register', register),
    path('users', users),

]