from django.urls import path

import authentication.views
import taskManagement.views

urlpatterns = [
    path('auth/login', authentication.views.logIn, name='login'),
    path('auth/signup', authentication.views.signUp, name='signup'),
    path('auth/change_password', authentication.views.reset_password, name='change-password'),
    path('auth/forgot_password', authentication.views.forgot_password, name='forgot-password'),
    path('auth/generate_otp', authentication.views.get_OTP, name='get-otp'),
    path('auth/verifie_otp', authentication.views.validate_otp, name='validate-otp'),
    path('auth/logout', authentication.views.logOut, name='logout'),
    path('task/', taskManagement.views.get_tasks, name='get-tasks'),
    path('task/add/', taskManagement.views.add_task, name='add-task'),
    path('task/edit/<int:id>', taskManagement.views.edit_task, name='edit-task'),
    path('task/delete/<int:id>', taskManagement.views.delete_task, name='delete-task'),
    path('task/<int:id>/comment', taskManagement.views.get_comments, name='get-comment'),
    path('task/<int:id>/add-comment', taskManagement.views.addCommentToTask, name='add-comment')
]