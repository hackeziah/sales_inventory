from django.urls import path

from users.views import (
    register, users
)

urlpatterns = [
    path('register', register),
    path('users', users),

]