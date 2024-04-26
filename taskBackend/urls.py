from django.contrib import admin
from django.urls import path

import authentication.views
import taskManagement.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/login', authentication.views.logIn, name='login'),
    path('auth/signup', authentication.views.signUp, name='signup'),
    path('task/', taskManagement.views.get_tasks, name='get-tasks'),
    path('task/add/', taskManagement.views.add_task, name='add-task'),
    path('task/edit/<int:id>', taskManagement.views.edit_task, name='edit-task'),
    path('task/delete/<int:id>', taskManagement.views.delete_task, name='delete-task')
]
