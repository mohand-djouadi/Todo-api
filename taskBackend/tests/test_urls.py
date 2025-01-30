from django.test import TestCase
from django.urls import resolve, reverse
from authentication.views import *
from taskManagement.views import *

class TestUrls(TestCase):

    def test_authentication_urls(self):
        urls = [
            ('login', logIn),
            ('signup', signUp),
            ('change-password', reset_password),
            ('forgot-password', forgot_password),
            ('get-otp', get_OTP),
            ('validate-otp', validate_otp),
            ('logout', logOut),
        ]
        for name, view in urls:
            with self.subTest(name=name):
                self.assertEqual(resolve(reverse(name)).func, view)

    def test_task_urls(self):
        urls = [
            ('get-tasks', get_tasks),
            ('add-task', add_task)
        ]
        urls_param = [
            ('get-task', get_task, {'id':1}),
            ('edit-task', edit_task, {'id':1}),
            ('delete-task', delete_task, {'id':1}),
            ('get-comment', get_comments, {'id':1}),
            ('add-comment', addCommentToTask, {'id':1})
        ]
        for name, view in urls:
            with self.subTest(name=name):
                self.assertEqual(resolve(reverse(name)).func, view)
        for name, view, kwargs in urls_param:
            with self.subTest(name=name):
                self.assertEqual(resolve(reverse(name, kwargs=kwargs)).func, view)