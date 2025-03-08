from django.test import TestCase
from authentication.models import User
from taskManagement.models import Task, Comment
from datetime import timedelta, datetime, timezone
import pytz

timezone = pytz.timezone('Europe/Paris')

class testUsersModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='mohand.djouadi',
            first_name='mohand',
            last_name='djouadi',
            password='Mohand100%',
            quest_label='what is your favorite movie',
            sec_answ='the maze runner',
            email='djouadimohand&2gmail.com',
        )
    def test_create_user(self):
        self.assertEqual(self.user.username, 'mohand.djouadi')
        self.assertEqual(self.user.first_name, 'mohand')
        self.assertEqual(self.user.last_name, 'djouadi')
        self.assertEqual(self.user.security_quest, 'QUESTION_1')
        self.assertNotEqual(self.user.password, 'Mohand100%')
        self.assertTrue(self.user.check_password('Mohand100%'), self.user.password)
    def test_read_user(self):
        user = User.objects.get(id=self.user.id)
        self.assertEqual(user.username, self.user.username)
        self.assertEqual(user.first_name, self.user.first_name)
        self.assertEqual(user.last_name, self.user.last_name)
        self.assertEqual(user.security_quest, self.user.security_quest)
        self.assertEqual(user.password, self.user.password)
    def test_update_user(self):
        self.user.set_password('New Test %password123%')
        self.user.email = 'mohand.djouadi@fgei.ummto.dz'
        self.user.save()
        self.assertEqual(self.user.email, 'mohand.djouadi@fgei.ummto.dz')
        self.assertTrue(self.user.check_password('New Test %password123%'), self.user.password)
    def test_delete_user(self):
        user_id = self.user.id
        self.user.delete()
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=user_id)
    def test_security_label(self):
        self.assertEqual(self.user.get_security_quest_value('what is your favorite movie'), 'QUESTION_1')
        self.assertEqual(self.user.get_security_quest_value('what is your first animal companion'), 'QUESTION_2')
        self.assertEqual(self.user.get_security_quest_value('what is your mother\'s name'), 'QUESTION_3')
        self.assertEqual(self.user.get_security_quest_value('what is your childhood nickname'), 'QUESTION_4')
        self.assertEqual(self.user.get_security_quest_value('what is the name of your best teacher'), 'QUESTION_5')
    def test_security_value(self):
        self.assertEqual(self.user.get_Security_quest_label('QUESTION_1'), 'what is your favorite movie')
        self.assertEqual(self.user.get_Security_quest_label('QUESTION_2'), 'what is your first animal companion')
        self.assertEqual(self.user.get_Security_quest_label('QUESTION_3'), 'what is your mother\'s name')
        self.assertEqual(self.user.get_Security_quest_label('QUESTION_4'), 'what is your childhood nickname')
        self.assertEqual(self.user.get_Security_quest_label('QUESTION_5'), 'what is the name of your best teacher')

class testTasksModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='mohand.djouadi',
            first_name='mohand',
            last_name='djouadi',
            password='Mohand100%',
            quest_label='what is your favorite movie',
            sec_answ='the maze runner',
            email='djouadimohand&2gmail.com',
        )
        timezone = pytz.timezone('Europe/Paris')
        task_datetime = timezone.localize(datetime(2025, 1, 5, 1, 0, 0))
        self.task = Task.objects.create(
            title='unit tests',
            description='write unite test for url models ans view for the django todo api project',
            location='home',
            taskDate=task_datetime,
            user=self.user
        )
    def test_create_task(self):
        self.assertEqual(self.task.title, 'unit tests')
        self.assertEqual(self.task.description, 'write unite test for url models ans view for the django todo api project')
        self.assertEqual(self.task.location, 'home')
        self.assertEqual(self.task.status, 'NOT_STARTED')
        self.assertEqual(self.task.taskDate, timezone.localize(datetime(2025, 1, 5, 1, 0, 0)))
        self.assertEqual(self.task.user, self.user)
    def test_read_task(self):
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.title, self.task.title)
        self.assertEqual(task.taskDate, self.task.taskDate)
        self.assertEqual(task.description, self.task.description)
        self.assertEqual(task.location, self.task.location)
        self.assertEqual(task.status, self.task.status)
        self.assertEqual(task.user, self.task.user)
    def test_update_task(self):
        self.task.location = 'cafe'
        self.task.save()
        self.assertEqual(self.task.location, 'cafe')
    def test_delete_task(self):
        task_id = self.task.id
        self.task.delete()
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=task_id)
    def test_status_value(self):
        self.assertEqual(Task.get_status_value('Not started'), 'NOT_STARTED')
        self.assertEqual(Task.get_status_value('In progress'), 'IN_PROGRESS')
        self.assertEqual(Task.get_status_value('Pending'), 'PENDING')
        self.assertEqual(Task.get_status_value('Completed'), 'COMPLETED')
        self.assertEqual(Task.get_status_value('On hold'), 'ON_HOLD')
        self.assertEqual(Task.get_status_value('Canceled'), 'CANCELED')
    def test_update_fields(self):
        kwargs = { "title":"test updates", "location":"home", "status":"In progress" }
        self.task.update_fields(**kwargs)
        self.assertEqual(self.task.title, kwargs.get("title"))
        self.assertEqual(self.task.location, kwargs.get("location"))
        self.assertEqual(self.task.status, Task.get_status_value(kwargs.get("status")))


    


class testCommentModel(TestCase):

    def setUp(self):
        self.task = Task.objects.create(
            title='test task',
            taskDate='2024-11-24 01:00:00+01',
            description='this is just for unite tests for this model',
        )
        self.comment = Comment.objects.create(content='this is test comment', task=self.task)

    def test_create_comment(self):
        self.assertEqual(self.comment.content, 'this is test comment')
        self.assertEqual(self.comment.task, self.task)
        now = datetime.now(pytz.utc)
        self.assertAlmostEqual(self.comment.createdAt, now, delta=timedelta(seconds=1))
    def test_read_comment(self):
        comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(self.comment.id, comment.id)
        self.assertEqual(self.comment.content, comment.content)
    def test_update_comment(self):
        self.comment.content = 'this is update test comment'
        self.comment.save()
        self.assertEqual(self.comment.content, 'this is update test comment')
    def test_delete_comment(self):
        comment_id = self.comment.id
        self.comment.delete()
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(id=comment_id)
    def test_delete_task_for_comment(self):
        comment_id = self.comment.id
        self.task.delete()
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(id=comment_id)
